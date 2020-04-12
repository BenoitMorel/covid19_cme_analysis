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
using namespace genesis::tree;
using namespace genesis::utils;

#include <algorithm>
#include <limits>
#include <map>

int main( int argc, char** argv )
{
    // Activate logging.
    utils::Logging::log_to_stdout();
    utils::Logging::details.time = true;
    LOG_INFO << "Started";

    // Get the files from command line
    if( argc != 4 ) {
        throw std::runtime_error(
            std::string( "Usage: " ) + argv[0] + " <input-tree-newick> <input-metadata-csv> <output-tree-prefix>"
        );
    }
    auto const tree_file = std::string( argv[1] );
    auto const meta_file = std::string( argv[2] );
    auto const out_prefix = std::string( argv[3] );

    // Read tree
    auto const tree = CommonTreeNewickReader().read( from_file( tree_file ));
    LOG_INFO << "Found tree with " << leaf_node_count( tree ) << " tips in tree file";

    // Test. Print all leaf node names.
    // for( auto const& node : tree.nodes() ) {
    //     if( is_leaf(node) ) {
    //         LOG_BOLD << node.data<CommonNodeData>().name;
    //     }
    // }

    // Read metadata. We use the default reader settings, which assumes the first row contains
    // the column names of the metadata fields, and the first column contains the names that
    // correspond to the tree leaf names.
    auto data = DataframeReader<std::string>().read( from_file( meta_file ));
    LOG_INFO << "Found " << data.cols() << " meta data columns with " << data.rows() << " entries.";

    // For each column, make a new tree visualization
    for( size_t i = 0; i < data.cols(); ++i ) {

        // Prepare a vector that collects all values for the edges, which we use to aggregate
        // and average for the inner edges of the tree, so that they represent their subtrees.
        // Each entry corresponds to an edge index, and contains the sum of all values in the subtree
        // in the first element of the pair, and the number of edges in the subtree in the second
        // element of the pair.
        // For example: An edge that leads to a leaf node contains just its metadata value and 1
        // edge count, while an edge that leads to a cherry contains the sum of both edges below
        // it and the count 2.
        // By doing this, we can easily aggregate and calculate averages later.
        std::vector<std::pair<double, size_t>> edge_values( tree.edge_count() );

        // Also, when the column cannot be converted to numbers, we cannot make a color gradient
        // as a legend next to the tree, but instead want a simple list of colors. So, for this case,
        // we here prepare a list of labels for this color list, and fill it if we find a string
        // column. In that case, a filled list is later used as an indicator that we indeed want to
        // make a list instead of a gradient.
        std::vector<std::string> color_labels;

        // In order to map values to colors, we need the min and max value that occur in the column,
        double min_value = std::numeric_limits<double>::infinity();
        double max_value = -std::numeric_limits<double>::infinity();

        // Convert metadata to numercial where possible. In the future, we can also do other data types,
        // bool, int, tine/data, geo location, etc...
        // Then, fill the edge values with the data
        if( is_convertible_to_double( data, i )) {
            convert_to_double( data, i );
            LOG_INFO << summarize_column( data, i );
            auto const& data_col = data[i].as<double>();

            for( size_t e = 0; e < tree.edge_count(); ++e ) {
                if( is_leaf( tree.edge_at(e)) ) {
                    auto const& name = tree.edge_at(e).secondary_node().data<CommonNodeData>().name;
                    if( !data.has_row_name( name ) ) {
                        throw std::runtime_error( "No metadata row for leaf node " + name );
                    }
                    edge_values[e] = { data_col[name], 1 };
                    min_value = std::min(min_value, data_col[name]);
                    max_value = std::max(max_value, data_col[name]);
                }
            }
        } else {
            // If we are here, we have a column that cannot be converted to numbers.
            // Treat it as a list of strings, where we visualize each string with its own color.
            // For this, we make a list of them, sort it, and give colors in alphabetical order.
            // In the future, we can also give colors in some other order that looks better
            // or makes more sense (country names ordered by location, for example).
            LOG_INFO << summarize_column( data, i );

            auto const& data_col = data[i].as<std::string>();

            // Make a map of all strings in the column, sorted. Then, give them their corresponding
            // index. We could use a sorted vector for this, but lookup would be slower than
            // using a map.
            std::map<std::string, size_t> value_map;
            for( auto const& v : data_col ) {
                value_map[v] = 0;
            }
            size_t cnt = 0;
            for( auto& v : value_map ) {
                color_labels.push_back( v.first );
                v.second = cnt;
                ++cnt;
            }
            min_value = 0;
            max_value = value_map.size() - 1;

            // Fill the edge values with the values the we just mapped to numbers
            for( size_t e = 0; e < tree.edge_count(); ++e ) {
                if( is_leaf( tree.edge_at(e)) ) {
                    auto const& name = tree.edge_at(e).secondary_node().data<CommonNodeData>().name;
                    if( !data.has_row_name( name ) ) {
                        throw std::runtime_error( "No metadata row for leaf node " + name );
                    }
                    edge_values[e] = { value_map[data_col[name]], 1 };
                }
            }
        }

        // Init with grey
        auto edge_colors = std::vector<Color>( tree.edge_count(), Color( 0.9, 0.9, 0.9 ));

        // Prepare a color mapping and a color normalization that brings all values between
        // min and max into the [0, 1] interval, so that we can nicely interpolate between them.
        auto map = ColorMap( color_list_nextstrain() );
        auto norm = ColorNormalizationLinear( min_value, max_value );

        // Now, we do a postorder traversal, filling in the inner edges with the average values
        // of their subtrees.
        for( auto const& it : postorder( tree )) {
            if( it.is_last_iteration() ) {
                continue;
            }
            if( is_leaf( it.edge() ) ) {
                if( edge_values[it.edge().index()].second != 1 ) {
                    LOG_DBG << "something is wrong with the edge indices for leaf nodes";
                }
            } else {
                if( edge_values[it.edge().index()].second != 0 ) {
                    LOG_DBG << "something is wrong with the edge indices for inner nodes";
                }
            }

            // We might have multifurcating trees, so we have to loop the full node here.
            // Loop over all edges of the subtrees of the current edge, and aggregate their values.
            for( auto const& nit : node_links( it.node() ) ) {
                // We skip the first iteration, which corresponds to the edge towards the root.
                // We are not doing this one yet.
                if( nit.is_first_iteration() ) {
                    continue;
                }
                if( edge_values[nit.edge().index()].second == 0 ) {
                    LOG_DBG << "something is wrong with the edge indices for aggregates";
                }

                edge_values[it.edge().index()].first += edge_values[nit.edge().index()].first;
                edge_values[it.edge().index()].second += edge_values[nit.edge().index()].second;
            }

            // Now we have all values for the current edge, and can hence calculate its color.
            double const value
                = edge_values[it.edge().index()].first
                / static_cast<double>( edge_values[it.edge().index()].second )
            ;
            edge_colors[it.edge().index()] = map( norm, value );
        }

        // Draw the tree. Params can be adjusted if needed, e.g., stroke width for the svg
        LayoutParameters params;
        params.stroke.width = 8.0;
        if( color_labels.empty() ) {
            write_color_tree_to_svg_file(
                tree, params, edge_colors, map, norm,
                out_prefix + data[i].name() + ".svg"
            );
        } else {
            write_color_tree_to_svg_file(
                tree, params, edge_colors, map.color_list( color_labels.size() ), color_labels,
                out_prefix + data[i].name() + ".svg"
            );
        }
    }

    LOG_INFO << "Finished";
    return 0;
}
