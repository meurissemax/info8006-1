%% Additional script
% This script makes it possible to display the results obtained in bar
% graph form in order to compare them.

% Project for the course INFO8006
% Authors: Maxime Meurisse & Valentin Vermeylen
% Academic year 2018-2019


%% Adding path
addpath(genpath('figures/'));
addpath('functions/');


%% Data setting
bars = {'Dumby', 'Greedy', 'Smarty'};

algos = {'Minimax', 'Alpha-beta', 'H-Minimax'};
results = [];

bar_title = '';
bar_xlabel = '';
bar_ylabel = '';

width = 0.9;

figname = '';
folder = 'figures/minimax/';

ylog = 0;


%% Data verification
nb_bars = size(bars, 2);

nb_algos = size(algos, 2);
nb_results = size(results);

if nb_results(1) ~= nb_bars
    error('Error in data verification');
end

if nb_results(2) ~= nb_algos
    error('Error in data verification');
end


%% Bar plot
x = categorical(bars);

fig = figure;

figproperties(bar(x, results, width), 'plot');

if ylog == 1
    set(gca, 'YScale', 'log')
end

figproperties(title(bar_title), 'title');
figproperties(xlabel(bar_xlabel), 'label');
figproperties(ylabel(bar_ylabel), 'label');

figproperties(legend(algos), 'legend');

%grid on

savesvg(fig, figname, folder);


%% Deleting unnecessary variables
clearvars -except bars algos results
