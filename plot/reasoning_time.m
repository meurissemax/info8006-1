%% Additional script
% This script makes it possible to display the results obtained.

% Project for the course INFO8006
% Authors: Maxime Meurisse & Valentin Vermeylen
% Academic year 2018-2019


%% Adding path
addpath(genpath('figures/'));
addpath('functions/');
addpath(genpath('results/'));


%% Data setting
filename = ["w1_p03", "w1_p05", "w1_p07"];
figname = 'w1';
iteration = 100;

folder = strcat('figures/reasoning_time/', num2str(iteration), '/');
number = length(filename);
data = cell(number, 1);

for i = 1:number
    fileID = fopen(strcat('results/reasoning_time/', num2str(iteration), '/', filename(i), '.txt'), 'r');
    data{i, 1} = fscanf(fileID, '%f');
    fclose(fileID);
end


%% Plot
bar_title = ['Entropy for w = ', num2str(data{1, 1}(1, 1)), ' with ', num2str(iteration), ' iterations'];
%bar_title = 'Entropy for p = 0';
bar_xlabel = 'Number of iterations';
bar_ylabel = 'Entropy';

fig = figure;

figproperties(title(bar_title), 'title');
figproperties(xlabel(bar_xlabel), 'label');
figproperties(ylabel(bar_ylabel), 'label');

set(gca, 'XLim', [0 iteration]);

hold on

for i = 1:number
    y = data{i, 1}(3:length(data{i, 1}));
    x = 1:length(y);

    %figproperties(bar(x, y, 'FaceAlpha', 0.5, 'BarWidth', 0.5), 'plot');
    figproperties(plot(x, y), 'plot');
end

legend(['p = ', num2str(data{1, 1}(2, 1))], ['p = ', num2str(data{2, 1}(2, 1))], ['p = ', num2str(data{3, 1}(2, 1))]);
%legend('w = 0', 'w = 1', 'w = 3', 'w = 5', 'w = 7');

hold off

savesvg(fig, figname, folder);


%% Deleting unnecessary variables
clearvars -except data x
