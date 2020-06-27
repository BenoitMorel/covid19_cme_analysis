/*
    Genesis - A toolkit for working with phylogenetic data.
    Copyright (C) 2014-2020 Lucas Czech

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Contact:
    Lucas Czech <lucas.czech@h-its.org>
    Exelixis Lab, Heidelberg Institute for Theoretical Studies
    Schloss-Wolfsbrunnenweg 35, D-69118 Heidelberg, Germany
*/

#include "genesis/genesis.hpp"

using namespace genesis;
using namespace genesis::sequence;
using namespace genesis::tree;
using namespace genesis::utils;

#include <cstdlib>
#include <fstream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>

#ifdef GENESIS_OPENMP
#   include <omp.h>
#endif

int main( int argc, char** argv )
{
    // Activate logging.
    utils::Logging::log_to_stdout();
    utils::Logging::details.time = true;
    // utils::Logging::max_level( utils::Logging::LoggingLevel::kDebug3 );
    utils::Logging::max_level( utils::Logging::LoggingLevel::kInfo );

    // Set threading
    utils::Options::get().number_of_threads( utils::Options::get().guess_number_of_threads() );
    LOG_INFO << "Using " << utils::Options::get().number_of_threads() << " threads";

    // Get the files from command line
    if (argc != 6) {
        throw std::runtime_error(
            "Usage: " + std::string( argv[0] ) + " <in_newick_file> <in_fasta_file> "
            "<target_leaf_count> <max_pruned_clade_size> <out_file_prefix>\n"
            "max_pruned_clade_size = 0 is a special case, "
            "where the max_pruned_clade_size check is deactivated"
        );
    }
    auto const in_newick_file = std::string( argv[1] );
    auto const in_fasta_file = std::string( argv[2] );
    auto const target_leaf_count = static_cast<size_t>( std::stoi( argv[3] ));
    auto const max_pruned_clade_size = static_cast<size_t>( std::stoi( argv[4] ));
    auto const out_file_prefix = std::string( argv[5] );
    LOG_INFO << "Started";

    // General tree drawing params that we will need later
    LayoutParameters params;

    // -------------------------------------------------------------
    //     File input and prep
    // -------------------------------------------------------------

    // Read in the files
    auto const tree = CommonTreeNewickReader().read( from_file( in_newick_file ));
    LOG_INFO << "Found tree with " << leaf_node_count(tree) << " leaf nodes.";
    auto const aln = FastaReader().read( from_file( in_fasta_file ));
    if( ! is_alignment(aln) ) {
        throw std::runtime_error( "Input fasta is not an alignment (sequence lengths differ)." );
    }
    LOG_INFO << "Found alignment with " << aln.size() << " sequences.";

    // Build a map from sequence label to sites, for speed
    std::unordered_map<std::string, std::string> aln_map;
    for( auto const& seq : aln ) {
        if( aln_map.count(seq.label()) > 0 ) {
            throw std::runtime_error("Sequence duplicate: " + seq.label());
        }
        aln_map[ seq.label() ] = seq.sites();
    }

    auto all_counts = SiteCounts( "ACGT", aln[0].size() );
    all_counts.add_sequences(aln);
    LOG_INFO << "avg entr of input aln : " << average_entropy( all_counts, false, SiteEntropyOptions::kIncludeGaps );

    // -------------------------------------------------------------
    //     Compute entropy of subtrees
    // -------------------------------------------------------------

    // Collect the entropy of the sequences in each subtree
    auto subtree_entropies = std::vector<double>( tree.link_count(), -1.0 );

    // Also, for each subtree, collect the indices of all its leaf nodes, and a bitvector
    // that keeps track of all edges that are part of that subtree (by setting their edge index)
    auto subtree_leaf_nodes = std::vector<std::vector<size_t>>( tree.link_count() );
    auto subtree_edges = std::vector<Bitvector>( tree.link_count() );

    // Compute the entropy of all subtrees
    LOG_INFO << "Compute the entropy of all " << subtree_entropies.size() << " subtrees";
    size_t subtree_cnt = 0;
    #pragma omp parallel for
    for( size_t i = 0; i < tree.link_count(); ++i ) {

        // No need for single edge subtrees
        if( is_leaf( tree.link_at( i ))) {
            continue;
        }

        // Init a sequence counter, that collects which nucleotides at which position appear how often
        auto counts = SiteCounts( "ACGT", aln[0].size() );

        // Init bitvector that contains all edges of the subtree
        subtree_edges[i] = Bitvector( tree.edge_count() );

        // Get the indices of all edges in the subtree, iterate it, and sum up all nucleotides
        // that we find in there. There are more efficient ways, but for the small data,
        // this works, and is easier to understand.
        auto const edge_indices = get_subtree_edges( tree.link_at( i ));
        for( auto edge_idx : edge_indices ) {
            subtree_edges[i].set( edge_idx );

            auto const& edge = tree.edge_at( edge_idx );
            if( ! is_leaf( edge )) {
                continue;
            }
            subtree_leaf_nodes[i].push_back( edge.secondary_node().index() );

            auto const& name = edge.secondary_node().data<CommonNodeData>().name;
            if( aln_map.count(name) == 0 ) {
                throw std::runtime_error( "Leaf name " + name + " not found in alignment." );
            }

            counts.add_sequence( aln_map.at( name ));
        }

        // If there are more than the max specified clade size, we do not want to consider that
        // clade at all, so let's just skip it.
        if( max_pruned_clade_size != 0 && subtree_leaf_nodes[i].size() > max_pruned_clade_size ) {
            LOG_DBG1 << "skipping subtree with " << subtree_leaf_nodes[i].size() << " leaves";
            continue;
        }
        LOG_DBG1 << "using    subtree with " << subtree_leaf_nodes[i].size() << " leaves";

        subtree_entropies[i] = average_entropy( counts, false, SiteEntropyOptions::kIncludeGaps );
        ++subtree_cnt;
    }
    LOG_DBG1 << "collected entropy of " << subtree_cnt << " subtrees";

    // Visualize the tree with all its entropy values.
    // Naturally, as this is a tree with ent. values, we call it treebeard.
    auto treebeard = tree;
    for( auto& edge : treebeard.edges() ) {
        auto const p_ent = std::to_string( subtree_entropies[edge.primary_link().index()] );
        auto const s_ent = std::to_string( subtree_entropies[edge.secondary_link().index()] );
        edge.secondary_node().data<CommonNodeData>().name = s_ent + " / " + p_ent;
    }
    write_tree_to_svg_file( treebeard, params, out_file_prefix + "_entropy_tree.svg" );

    // -------------------------------------------------------------
    //     Find low entropy subtrees
    // -------------------------------------------------------------

    // Get the sorted entropies, from smalles to largest. We only get the sorting order here,
    // without actually sorting the list, so that we keep the indices to the subtrees correct.
    auto const entropy_sorting = sort_indices( subtree_entropies.begin(), subtree_entropies.end() );

    // List of all subtrees (by their link index) that we pick to be pruned (i.e., combinded
    // into one single leaf representative)
    std::unordered_set<size_t> picked_subtrees;

    // We move along the sorted subtree entropy list and chose candidates from there.
    // Use this variable to store the index into entropy_sorting of the current candidate.
    // We first skip all the -1 entries that come from tip edges.
    size_t current_sorted_cand = 0;
    while( subtree_entropies[entropy_sorting[current_sorted_cand]] < 0.0 ) {
        ++current_sorted_cand;
    }
    if( current_sorted_cand == 0 ) {
        throw std::runtime_error( "no unset entropy values. this cannot be." );
    }
    LOG_DBG1 << "skipped to index " << current_sorted_cand << " of "
             << subtree_entropies.size() << " (" << entropy_sorting.size() << ")";

    // Iterate all candidate clades, and stop either if we have pruned away enough,
    // or, if we pruned all available ones, stop there as well (which means, that the max_pruned_clade_size
    // was set to a value that is too small to actually reach the target number of leaves)
    LOG_INFO << "Selecting candidate subtrees for pruning";
    size_t iter = 0;
    size_t current_leaf_count = leaf_node_count(tree);
    for(
        ;
        current_leaf_count > target_leaf_count && current_sorted_cand < entropy_sorting.size() ;
        ++current_sorted_cand
    ) {
        ++iter;
        auto const current_cand_link_idx = entropy_sorting[current_sorted_cand];

        LOG_DBG1 << "At iteration " << iter << " with candidate " << current_cand_link_idx << " with "
                 << current_leaf_count << " leaves remaining";
        LOG_DBG2 << "candidate subtree has entropy of " << subtree_entropies[current_cand_link_idx]
                 << " and a subtree with " << subtree_leaf_nodes[current_cand_link_idx].size() << " leaves";

        // Check if this candidate brings us below the target. If so, this is too much - we aim for
        // an exact hit (might change that later and introduce a valid range threshold instead).
        // (we do the comparison by addition instead of subtracting from the current_leaf_count,
        // to avoid integer underflow).
        // if( target_leaf_count + subtree_leaf_nodes[current_cand_link_idx].size() > current_leaf_count ) {
        //     LOG_DBG2 << "candidate subtree has " << subtree_leaf_nodes[current_cand_link_idx].size()
        //     << " leaves, which would bring us below the target_leaf_count " << target_leaf_count << ", so we skip";
        //     continue;
        // }

        // See if the candidate overlaps with any of the previously picked subtrees.
        // There are several scenarios here:
        // 1. they are completely disjunct.
        // 2. the current candidate is completely covered by a previously picked subtree.
        // 3. vice versa: the current candidate completely covers a previously picked subtree.
        // 4. they share some inner branches, but no leaves.
        //
        // the first case is the "do nothing" case. case two and thress: simply take the larger one,
        // remove the other one. case four: we skip, as this would lead to conflict.

        // keep track of the actions that we might need to perform: either skip the current
        // candidate (not prune it), or remove previous candidates again from the list
        // (in case they are fully covered by the current candidate subtree).
        bool skip_cand = false;
        std::vector<size_t> replace_prev;

        // test each previously picked subtree, by comparing their bitvectors
        // auto const cand_edge_idx = tree.link_at( current_cand_link_idx ).edge().index();
        LOG_DBG2 << "checking candidate " << current_cand_link_idx << " against "
                 << picked_subtrees.size() << " previously picked subtrees";
        for( auto prev_sub_link_idx : picked_subtrees ) {

            auto const& cbv = subtree_edges[current_cand_link_idx];
            auto const& pbv = subtree_edges[prev_sub_link_idx];
            // LOG_DBG3 << "checking candidate " << current_cand_link_idx << " against previous " << prev_sub_link_idx;

            if( (cbv & pbv).count() == 0 ) {
                // LOG_DBG3 << "1: no overlap";

                // case 1: no overlap. we can simply skip, nothing to do here. let's move on to
                // the next subtree to be tested
                // continue;
            }
            if( is_subset( cbv, pbv ) ) {
                LOG_DBG3 << "2: candidate covered by previous subtree " << prev_sub_link_idx
                         << " (which has " << subtree_leaf_nodes[prev_sub_link_idx].size() << " leaves)";

                // some error check
                if( skip_cand || !replace_prev.empty() ) {
                    LOG_WARN << "previous skip!";
                }

                // case 2: candidate is completely covered already. we can skip this whole candidate
                skip_cand = true;

                // Do not break for now, so that we can debug more
                // break;
            }
            if( is_subset( pbv, cbv ) ) {
                LOG_DBG3 << "3: previous subtree (" << prev_sub_link_idx << ", which has "
                         << subtree_leaf_nodes[prev_sub_link_idx].size() << " leaves) covered by candidate";

                // some error check
                if( skip_cand ) {
                    LOG_WARN << "and skip true!";
                }

                // case 3: the candidate covers another previously picked subtree. we
                // need to replace that subtree by the candidate. store the index in the picked list
                replace_prev.push_back( prev_sub_link_idx );

                // Do not break for now, so that we can debug more
                // break;
            }
            if( !is_subset( cbv, pbv ) && !is_subset( pbv, cbv ) && (cbv & pbv).count() > 0 ) {
                LOG_DBG3 << "4: collision: overlap of inner branches";

                // some error check
                if( skip_cand || !replace_prev.empty() ) {
                    LOG_WARN << "multiple subtrees in picked list collide with candidate!";
                }

                // case 4: overlap of inner branches. this is a conflict, and we skip the candidate,
                // hence keeping and preferring the previously picked subtree that had lower entropy
                skip_cand = true;
            }
        }

        // we are done checking against all previously picked subtrees. time for the verdict
        if( skip_cand ) {
            LOG_DBG2 << "skipping candidate " << current_cand_link_idx;
        } else {

            // Remove all previously picked subtrees that will be covered by the new one.
            for( auto rep_pre : replace_prev ) {
                LOG_DBG2 << "replacing subtree " << rep_pre <<  " with subtree " << current_cand_link_idx;

                // Update the current leaf count, so that we keep track of when we have pruned enough.
                // Add back the leaves of the subtree that we are about to remove from the list,
                // and subtract the leaves of the new candidate. Minus one, because each one of
                // them would have been represented by one leaf in the end.
                current_leaf_count += subtree_leaf_nodes[ rep_pre ].size() - 1;

                // Remove the colliding one
                picked_subtrees.erase(rep_pre);
            }

            // Insert the new one, and update the current count, minus one, because we are going
            // to represent the subtree by one node in the end.
            LOG_DBG2 << "adding candidate " << current_cand_link_idx << " to picked list";
            current_leaf_count -= subtree_leaf_nodes[ current_cand_link_idx ].size() - 1;
            if( picked_subtrees.count(current_cand_link_idx) > 0 ) {
                throw std::runtime_error("candidate already inserted");
            }
            picked_subtrees.insert(current_cand_link_idx);
        }
    }

    LOG_INFO << "ended with current_leaf_count " << current_leaf_count << " by pruning "
             << picked_subtrees.size() << " subtrees";

    if( current_leaf_count > target_leaf_count ) {
        LOG_WARN << "this is more than was specified by <target_leaf_count> = " << target_leaf_count
                 << ", which means that we could not find enough clades for pruning. you have to "
                 << "increase the value of <max_pruned_clade_size> to get down to the desired "
                 << "number of leaf taxa!";
    }

    // -------------------------------------------------------------
    //     Visualize resulting pruned tree
    // -------------------------------------------------------------

    // Color list with enough colors for all picked trees.
    auto const color_list = ColorMap( color_list_nextstrain() ).color_list( picked_subtrees.size() );
    auto color_labels = std::vector<std::string>();

    LOG_INFO << "writing prune tree visualization";
    auto edge_colors = std::vector<Color>( tree.edge_count(), Color(0.8, 0.8, 0.8) );
    size_t i = 0;
    for( auto subtree_idx : picked_subtrees ) {
        color_labels.push_back( std::to_string(subtree_idx) );
        LOG_DBG1 << "subtree " << subtree_idx << " selected for pruning, which has "
                 << subtree_leaf_nodes[subtree_idx].size() << " leaves and entropy "
                 << subtree_entropies[subtree_idx];

        for( size_t j = 0; j < subtree_edges[subtree_idx].size(); ++j ) {
            if( subtree_edges[subtree_idx][j] ) {
                edge_colors[j] = color_list[i];
            }
        }
        ++i;
    }

    write_color_tree_to_svg_file(
        tree, params, edge_colors, color_list, color_labels, out_file_prefix + "_pruning_tree.svg"
    );

    // -------------------------------------------------------------
    //     Pick representative sequences for each pruned subtree
    // -------------------------------------------------------------

    // helper function that measures how well a sequence represents the consensus of a clade
    auto match_score = []( std::string const& consensus, std::string const& candidate )
    {
        if( consensus.size() != candidate.size() ) {
            throw std::runtime_error( "Comparing apples and oranges." );
        }

        size_t matches = 0;
        for( size_t i = 0; i < consensus.size(); ++i ) {
            auto const amb = nucleic_acid_ambiguities( consensus[i] );
            if( amb.find( candidate[i] ) != std::string::npos ) {
                ++matches;
            }
        }
        return matches;
    };

    // collect the sequences that we prune away. we need them later, if we did not exaclty
    // hit the correct number of taxa.
    std::vector<std::pair<std::string, std::string>> removed_seqs;

    // go through all picked subtrees that we want to prune, find the sequence within each of them
    // that best represents its respective subtree, and use it as a replacement for all sequences
    // in the subtree
    LOG_INFO << "compute consensus and pick best representatives for each subtree";
    for( auto subtree_idx : picked_subtrees ) {
        auto const& subtree_nodes = subtree_leaf_nodes[ subtree_idx ];
        LOG_DBG1 << "replacing subtree " << subtree_idx << " with " << subtree_nodes.size() << " leaves";

        // Compute consensus sequence for the subtree
        auto counts = SiteCounts( "ACGT", aln[0].size() );
        for( auto node_idx : subtree_nodes ) {
            auto const& name = tree.node_at(node_idx).data<CommonNodeData>().name;
            counts.add_sequence( aln_map.at( name ));
        }
        auto const subtree_consensus = consensus_sequence_with_threshold( counts );

        // find the sequence of the subtree that best represents it
        size_t best_score = 0;
        size_t best_node_idx = 0;
        for( auto node_idx : subtree_nodes ) {
            auto const& name = tree.node_at(node_idx).data<CommonNodeData>().name;

            auto const score = match_score( subtree_consensus, aln_map[name] );
            if( score > best_score ) {
                best_score = score;
                best_node_idx = node_idx;
            }
            LOG_DBG2 << "leave " << name << " got score " << score;
        }

        // delete all others from the alignment
        for( auto node_idx : subtree_nodes ) {
            auto const& name = tree.node_at(node_idx).data<CommonNodeData>().name;
            if( node_idx == best_node_idx ) {
                LOG_DBG2 << "winner " << name;
            } else {
                removed_seqs.emplace_back( name, aln_map[name] );
                aln_map.erase( name );
            }
        }
    }

    // Add back pruned sequences to fill up to exactly the desired leaf count.
    if( current_leaf_count < target_leaf_count ) {
        LOG_INFO << "as the current number of remaining leave nodes " << current_leaf_count
                 << " is below the desired number " << target_leaf_count
                 << ", we now add some more sequences picked from the pruned subtrees until "
                 << "we reach exactly the correct number of leaves. "
                 << "we pick sequences so that they maximize entropy.";

        // create site counts object as a base for entropy calclation
        auto base_counts = SiteCounts( "ACGT", aln[0].size() );
        for( auto const& seq : aln_map ) {
            base_counts.add_sequence( Sequence( seq.first, seq.second ));
        }
        LOG_INFO << "avg entr of base aln : " << average_entropy(
            base_counts, false, SiteEntropyOptions::kIncludeGaps
        );

        // Not very efficient, but get's the job done for now.
        while( current_leaf_count < target_leaf_count ) {
            LOG_DBG1 << "adding more sequences to get from current_leaf_count=" << current_leaf_count
                     << " to target_leaf_count=" << target_leaf_count;

            // find sequence that maximized entropy of resulting set. we make a copy of the counts
            // object every time, which is so inefficient, but so convenient...
            size_t max_i = 0;
            double max_e = -1.0;
            #pragma omp parallel for
            for( size_t i = 0; i < removed_seqs.size(); ++i ) {

                // compute entropy of all currently selected sequences plus exactly one from
                // the removed ones.
                auto copy_counts = base_counts;
                auto const& r = removed_seqs[i];
                copy_counts.add_sequence( Sequence( r.first, r.second ));
                double entr = average_entropy(
                    copy_counts, false, SiteEntropyOptions::kIncludeGaps
                );

                // if this is larger than what we currently have, store it
                if( entr > max_e ) {
                    max_e = entr;
                    max_i = i;
                }
            }

            // Now we have traversed all sequences that were previously removed, and found the one
            // that maximized entropy. move it from the removed set to the result set.
            auto const& e = removed_seqs[max_i];
            LOG_DBG2 << "adding " << e.first;
            aln_map[ e.first ] = e.second;
            base_counts.add_sequence( Sequence( e.first, e.second ));
            removed_seqs.erase( removed_seqs.begin() + max_i );
            ++current_leaf_count;

            // we are done here. we iterate, and in the next iteration, that sequence is now part of
            // the base, and will be considered while we continue until we have added enough sequences.

            // old, random picking
            // auto const n = std::rand() % removed_seqs.size();
            // auto const& e = removed_seqs[n];
            //
            // LOG_DBG2 << "adding " << e.first;
            // aln_map[ e.first ] = e.second;
            // removed_seqs.erase( removed_seqs.begin() + n );
            // ++current_leaf_count;
        }
    }

    // -------------------------------------------------------------
    //     Write the pruned alignment
    // -------------------------------------------------------------

    LOG_INFO << "write out final alignment";
    auto const outfile = out_file_prefix + "_pruned_alignment.fasta";
    FastaOutputIterator fasta_out_it( to_file( outfile ));
    SequenceSet final_aln;
    for( auto const& seq : aln_map ) {
        fasta_out_it << Sequence( seq.first, seq.second );
        final_aln.add( Sequence( seq.first, seq.second ));
    }

    auto final_counts = SiteCounts( "ACGT", final_aln[0].size() );
    final_counts.add_sequences(final_aln);
    LOG_INFO << "avg entr of final aln : " << average_entropy(
        final_counts, false, SiteEntropyOptions::kIncludeGaps
    );

    LOG_INFO << "Finished";
    return 0;
}
