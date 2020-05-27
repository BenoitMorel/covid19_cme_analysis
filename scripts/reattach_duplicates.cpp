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

#include <string>
#include <unordered_map>
#include <vector>

int main( int argc, char** argv )
{
    // Activate logging.
    utils::Logging::log_to_stdout();
    utils::Logging::details.time = true;

    // Get the files from command line
    if (argc != 4) {
        throw std::runtime_error(
            "Need to provide an input and an output newick files, and a json file.\n"
        );
    }
    auto const newick_file = std::string( argv[1] );
    auto const output_newick_file = std::string( argv[2] );
    auto const json_file = std::string( argv[3] );
    LOG_INFO << "Started";

    // Read in the files
    auto tree = CommonTreeNewickReader().read( from_file( newick_file ));
    auto const seq_list = JsonReader().read( from_file( json_file ));
    LOG_INFO << "Found tree with " << leaf_node_count(tree) << " leaf nodes.";

    // Attach new leaf nodes to tree
    for( auto const& elem : seq_list.get_object() ) {
        if( ! elem.second.is_array() ) {
            throw std::runtime_error( "Invalid json map file with non-array list." );
        }

        // The key of the json object is a leaf node name. Find that node.
        auto node = find_node( tree, elem.first );
        if( node == nullptr ) {
            // throw std::runtime_error( "Cannot find node " + elem.first + " in tree." );
            LOG_WARN << "Cannot find node " + elem.first + " in tree. This probably means that the "
            << "according sequence was not used in the tree inference, and is hence skipped here.";
            continue;
        }

        // Now, to make that in inner node, we just set its name to an empty string,
        // and then attach new leaf nodes to it, with the full list of the json element,
        // which also contains the original leafe node name again that we just set to be empty,
        // so that it gets re-attached as a leaf node.
        node->data<CommonNodeData>().name = "";
        for( auto const& leaf : elem.second.get_array() ) {
            if( ! leaf.is_string() ) {
                throw std::runtime_error( "Invalid json map file with non-string name." );
            }
            auto& new_node = add_new_node( tree, *node );
            new_node.data<CommonNodeData>().name = leaf.get_string();
        }
    }

    // Write new newick file
    CommonTreeNewickWriter().write( tree, to_file( output_newick_file ));
    LOG_INFO << "Wrote tree with " << leaf_node_count(tree) << " leaf nodes.";

    LOG_INFO << "Finished";
    return 0;
}
