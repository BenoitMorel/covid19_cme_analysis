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

#include <string>

using namespace genesis;
using namespace genesis::sequence;

int main( int argc, char** argv )
{
    // Activate logging.
    utils::Logging::log_to_stdout();
    utils::Logging::details.time = true;

    // Get input
    if( argc != 2 ) {
        throw std::runtime_error( "Usage: " + std::string(argv[0]) + " <msa.fasta>" );
    }
    auto const infile = std::string(argv[1]);

    // Read input
    LOG_INFO << "Started";
    auto const seqs = FastaReader().read( utils::from_file( infile ));
    if( seqs.size() == 0 || ! is_alignment( seqs )) {
        throw std::runtime_error( "Input is not a usable MSA" );
    }

    // Aggregate sites
    auto counts = SiteCounts( "ACGT", seqs[0].size() );
    counts.add_sequences( seqs );

    LOG_INFO << "absolute_entropy:     " << absolute_entropy( counts );
    LOG_INFO << "average_entropy:      " << average_entropy( counts );
    LOG_INFO << "absolute_information: " << absolute_information( counts );
    LOG_INFO << "average_information:  " << average_information( counts );

    LOG_INFO << "Finished";
    return 0;
}
