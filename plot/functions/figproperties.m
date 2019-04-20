%% Additional function
% Function that defines the properties of the figures.

% Arguments:
%   - object: the object whose properties we want to define
%   - type: the type of the object

% Project for the course INFO8006
% Authors: MEURISSE Maxime
% Academic year 2018-2019

function figproperties(object, type)

% Plot
if strcmp(type, 'plot')
    set(gca,...
        'FontName', 'Arial',...
        'FontSize', 20,...
        'FontWeight', 'normal',...
        'FontSmoothing', 'on',...
        'GridAlpha', 0.3 ...
        );

    set(object,...
        'LineWidth', 0.5 ...
        );

    set(gcf,...
        'Position', get(0, 'Screensize')...
        );
end

% Title
if strcmp(type, 'title')
    set(object,...
        'FontName', 'Arial',...
        'FontSize', 28,...
        'FontWeight', 'bold',...
        'FontSmoothing', 'on'...
        );
end

% Label
if strcmp(type, 'label')
    set(object,...
        'FontName', 'Arial',...
        'FontSize', 20,...
        'FontWeight', 'normal',...
        'FontSmoothing', 'on'...
        );
end

% Legend
if strcmp(type, 'legend')
    set(object,...
        'FontName', 'Arial',...
        'FontSize', 26,...
        'FontWeight', 'normal'...
        );
end

end