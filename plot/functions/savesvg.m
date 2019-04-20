%% Additional function
% Function that saves a figure in SVG.

% Arguments:
%   - fig: the figure to save
%   - figname: the name of the figure

% Project for the course INFO8006
% Authors: MEURISSE Maxime
% Academic year 2018-2019

function savesvg(fig, filename, folder)

print(fig, strcat(folder, filename), '-dsvg');

end
