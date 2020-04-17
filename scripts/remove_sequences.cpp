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
using namespace genesis::utils;

#include <string>
#include <unordered_map>
#include <vector>
#include <sstream>
#include <string>
#include <fstream>

std::vector<std::string> get_nonempty_noncomment_lines( std::string const& file )
{
    std::string const comment_token("#");

    std::vector<std::string> res;

    std::ifstream infile(file);
    std::string line;

    while (std::getline(infile, line)) {
        // trim whitespace from left and right
        line = trim_right( trim_left( line ) );

        if( not line.empty()
            and not starts_with( line, comment_token ) ) {
            res.push_back( line );
        }
    }


    return res;
}

int main( int argc, char** argv )
{
    // Activate logging.
    utils::Logging::log_to_stdout();
    utils::Logging::details.time = true;

    // Get the files from command line
    if (argc != 5) {
        throw std::runtime_error(
            std::string( "Usage: " ) + argv[0] + " <input-msa> <exclude-file> <output-fasta> <excluded-fasta>"
        );
    }
    auto const infile = std::string( argv[1] );
    auto const exclude_file = std::string( argv[2] );
    auto const outfile = std::string( argv[3] );
    auto const trimmed_seqs = std::string( argv[4] );

    LOG_INFO << "Specified: infile = " << infile;
    LOG_INFO << "Specified: exclude_file = " << exclude_file;

    // parse the outgroup names
    auto excluded = get_nonempty_noncomment_lines( exclude_file );

    // output iterator for the retained sequences
    std::ofstream retained_out_stream;
    file_output_stream( outfile, retained_out_stream );
    FastaOutputIterator retained{ retained_out_stream };

    // output iterator for the removed sequences
    std::ofstream removed_out_stream;
    file_output_stream( outfile, removed_out_stream );
    FastaOutputIterator removed{ removed_out_stream };

    // Read the file
    LOG_INFO << "Started";
    auto fasta_in = FastaInputIterator( from_file( infile ));
    size_t cnt = 0;
    while( fasta_in ) {
        auto seq = *fasta_in;
        // replace_characters( seq, "Nn", '-' );

        if( seq.sites().empty() || seq.label().empty() ) {
            throw std::runtime_error( "Invalid sequences with empty label or sites." );
        }

        if( contains_ci( excluded, seq.label() ) ) {
            // removed case
            removed = seq;
            ++cnt;
        } else {
            // normal case
            retained = seq;
        }

        ++fasta_in;
    }
    // LOG_INFO << "Found " << cnt << " sequences, thereof " << seq_map.size() << " unique.";
    LOG_INFO << "Removed " << cnt << " seqeunces.";
    
    LOG_INFO << "Finished";
    return 0;
}
