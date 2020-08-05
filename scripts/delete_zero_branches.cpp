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

int main( int argc, char** argv )
{
    // Check if the command line contains the right number of arguments.
    if (argc != 2) {
        throw std::runtime_error(
            "Need to provide a newick tree file.\n"
        );
    }

    // Activate logging.
    utils::Logging::log_to_stdout();
    utils::Logging::details.time = true;

    auto newick_path = std::string( argv[1] );
    auto tree = CommonTreeNewickReader().read( utils::from_file( newick_path ));

    delete_zero_branch_length_edges( tree );

    CommonTreeNewickWriter().write( tree, utils::to_file( newick_path + ".nonzero" ));

    return 0;
}
