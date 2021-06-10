% GSPBOX - Embeddings
%
%  Availlable embeddings
%    gsp_lle                       -  Local Linear Embedding
%    gsp_laplacian_eigenmaps       -  Laplacian Eigenmaps
%    gsp_isomap                    -  Isomap
%    gsp_eigenspace_estimation     -  Fast Eigenspace Approximation using Random Signals (FEARS)
%
%  Utils
%    gsp_weight2distance           -  Distance matrix from weight matrix
%    gsp_compute_coordinates       -  Compute new coordinates for a graph
%
%  For help, bug reports, suggestions etc. please send email to
%  gspbox 'dash' support 'at' groupes 'dot' epfl 'dot' ch
%
%
%   Url: https://epfl-lts2.github.io/gspbox-html/doc/embedding/Contents.html

% Copyright (C) 2013-2016 Nathanael Perraudin, Johan Paratte, David I Shuman.
% This file is part of GSPbox version 0.7.5
%
% This program is free software: you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation, either version 3 of the License, or
% (at your option) any later version.
%
% This program is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU General Public License for more details.
%
% You should have received a copy of the GNU General Public License
% along with this program.  If not, see <http://www.gnu.org/licenses/>.

% If you use this toolbox please kindly cite
%     N. Perraudin, J. Paratte, D. Shuman, V. Kalofolias, P. Vandergheynst,
%     and D. K. Hammond. GSPBOX: A toolbox for signal processing on graphs.
%     ArXiv e-prints, Aug. 2014.
% http://arxiv.org/abs/1408.5781
