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

#include <cassert>
#include <string>
#include <unordered_map>
#include <vector>
#include <sstream>
#include <string>
#include <fstream>

std::vector<std::vector<std::string>> read_mptp_species_file( std::string const& file )
{
    std::vector<std::vector<std::string>> res;

    // Read the file
    auto const content = file_read_lines( file );

    // Skip the header
    size_t line = 0;
    while( line < content.size() && !content[line].empty() ) {
        ++line;
    }

    // Read each species list
    while( line < content.size() ) {
        // Skip empty lines
        if( content[line].empty() ) {
            ++line;
            continue;
        }

        // If the line starts with the keyword, add a new inner vector to the outer vector.
        // If not, it's a species, so append it to the last inner vector.
        // Let's hope that no species actually starts with the term "Species".
        // Fucking bioinformatics file formats.
        if( starts_with( content[line], "Species" )) {
            res.push_back({});
        } else {
            res.back().push_back( content[line] );
        }
        ++line;
    }

    return res;
}

int main( int argc, char** argv )
{
    // Activate logging.
    utils::Logging::log_to_stdout();
    utils::Logging::details.time = true;
    LOG_INFO << "Started";

    // Get the files from command line
    if( argc != 4 ) {
        throw std::runtime_error(
            std::string( "Usage: " ) + argv[0] + " <input-mptp-tree> <input-mptp-species> <output-tree>"
        );
    }
    auto const tree_file = std::string( argv[1] );
    auto const species_file = std::string( argv[2] );
    auto const outfile = std::string( argv[3] );

    // Read tree
    auto const tree = CommonTreeNewickReader().read( from_file( tree_file ));
    LOG_INFO << "Found tree with " << leaf_node_count( tree ) << " tips in tree file";

    // Read mptp
    auto const species = read_mptp_species_file( species_file );
    LOG_INFO << "Found " << species.size() << " species in mptp file";

    // Find the mptp species in the tree, and give them colors.
    auto edge_colors = std::vector<Color>( tree.edge_count(), Color( 0.9, 0.9, 0.9 ));
    auto const color_set = color_list_set1();
    for( size_t i = 0; i < species.size(); ++i ) {

        // Find all clades of the tree (i.e., groups of edge that are separated from the rest of
        // the tree) that only contain tips from the given list of species...
        auto const clade_edge_indices = find_monophyletic_subtree_edges( tree, species[i] );

        // ... and give them their own color
        for( auto edge_idx : clade_edge_indices ) {
            edge_colors[ edge_idx ] = color_set[i];
        }
    }

    // Draw the tree. Params can be adjusted if needed, e.g., stroke width for the svg
    LayoutParameters params;
    params.stroke.width = 8.0;
    write_color_tree_to_svg_file( tree, params, edge_colors, outfile );

    LOG_INFO << "Finished";
    return 0;
}
