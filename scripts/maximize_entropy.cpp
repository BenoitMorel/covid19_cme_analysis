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
    if (argc != 4) {
        throw std::runtime_error(
            "Usage: " + std::string( argv[0] ) + " <in_fasta_file> "
            "<target_leaf_count> <out_file_prefix>"
        );
    }
    auto const in_fasta_file = std::string( argv[1] );
    auto const target_leaf_count = static_cast<size_t>( std::stoi( argv[2] ));
    auto const out_file_prefix = std::string( argv[3] );
    LOG_INFO << "Started";

    // -------------------------------------------------------------
    //     File input and prep
    // -------------------------------------------------------------

    auto aln = FastaReader().read( from_file( in_fasta_file ));
    if( ! is_alignment(aln) ) {
        throw std::runtime_error( "Input fasta is not an alignment (sequence lengths differ)." );
    }
    LOG_INFO << "Found alignment with " << aln.size() << " sequences.";

    auto all_counts = SiteCounts( "ACGT", aln[0].size() );
    all_counts.add_sequences(aln);
    LOG_INFO << "avg entr of input aln : " << average_entropy( all_counts, false, SiteEntropyOptions::kIncludeGaps );

    // prepare result sequence set, as well as a counts for continuous entropy tracking
    SequenceSet result_aln;
    auto result_counts = SiteCounts( "ACGT", aln[0].size() );

    // -------------------------------------------------------------
    //     Pick first sequence to be far away from consensus
    // -------------------------------------------------------------

    // compute a consensus seq for the whole alignment.
    auto const consensus = consensus_sequence_with_threshold( all_counts );

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

    // go through all sequences, find the sequence that is furthest from the consensus seq
    // in the subtree
    size_t best_score = consensus.size() + 1;
    size_t best_seq = 0;
    for( size_t i = 0; i < aln.size(); ++i ) {
        auto const score = match_score( consensus, aln[i].sites() );
        if( score < best_score ) {
            best_score = score;
            best_seq = i;
        }
    }

    // Move the picked sequence to the result set.
    LOG_INFO << "best pick: " << best_seq << " " << aln[best_seq].label();
    result_aln.add( aln[best_seq] );
    result_counts.add_sequence( aln[best_seq] );
    aln.remove(best_seq);

    // -------------------------------------------------------------
    //     Fill up with entropy maximizing sequences
    // -------------------------------------------------------------

    // Not very efficient, but get's the job done for now.
    while( result_aln.size() < target_leaf_count ) {
        LOG_DBG1 << "at iteration " << result_aln.size() << " of " << target_leaf_count;
        // LOG_DBG1 << "adding more sequences to get from result_aln.size()=" << result_aln.size()
        //          << " to target_leaf_count=" << target_leaf_count;

        // find sequence that maximized entropy of resulting set. we make a copy of the counts
        // object every time, which is so inefficient, but so convenient...
        size_t max_i = 0;
        double max_e = -1.0;
        #pragma omp parallel for
        for( size_t i = 0; i < aln.size(); ++i ) {

            // compute entropy of all currently selected sequences plus exactly one from
            // the removed ones.
            auto copy_counts = result_counts;
            copy_counts.add_sequence( aln[i] );
            double entr = average_entropy(
                copy_counts, false, SiteEntropyOptions::kIncludeGaps
            );

            // if this is larger than what we currently have, store it
            #pragma omp flush( max_e )
            if( entr > max_e ) {
                #pragma omp critical( MAX_ENTR )
                if( entr > max_e ) {
                    max_e = entr;
                    max_i = i;
                }
            }
        }

        // Now we have traversed all sequences that were previously removed, and found the one
        // that maximized entropy. move it from the removed set to the result set.
        LOG_DBG2 << "adding " << aln[max_i].label();
        result_aln.add( aln[max_i] );
        result_counts.add_sequence( aln[max_i]);
        aln.remove( max_i );
    }

    // -------------------------------------------------------------
    //     Write the pruned alignment
    // -------------------------------------------------------------

    LOG_INFO << "write out final alignment";
    auto const outfile = out_file_prefix + "_pruned_alignment.fasta";
    FastaWriter().write( result_aln, to_file( outfile ));

    LOG_INFO << "avg entr of final aln : " << average_entropy(
        result_counts, false, SiteEntropyOptions::kIncludeGaps
    );

    LOG_INFO << "Finished";
    return 0;
}
