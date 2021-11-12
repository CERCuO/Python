classdef Tektronix_AWG610
    % driver for Tektronix AWG 610 arbitrary waveform generator
    % Developed by Daniel Hutama
    % Version 0.1 11 Nov 2021
    
    properties
        obj
        model
        gpib_addr
        info
    end 
    methods 
        function AWG = Tektronix_AWG610(VisaAddr, varargin)
            if ~isempty(varargin)
                AWG.info = varargin{1};
            else 
                AWG.info = '';
            end 
            AWG.model = 'Tektronix AWG 610'
            
            AWG.obj = visadev(VisaAddr)
        end 
        
        function GetInfo(AWG)
            tmp = query(AWG.obj, '*IDN?');
            disp(tmp)
        end 
        
    end 
end
            
            