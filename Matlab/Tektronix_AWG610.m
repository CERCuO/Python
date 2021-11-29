classdef Tektronix_AWG610
    % driver for Tektronix AWG 610 arbitrary waveform generator
    % Developed by Daniel Hutama
    % Version 0.1 11 Nov 2021
    % visadev needs Matlab R2021a or newer to work.
    
    % This device uses IEEE 488.2 
    % Standard Commands for Programmable Instruments (SCPI) 
    
    
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
            AWG.model = 'Tektronix AWG 610';
            AWG.manualURL = 'https://download.tek.com/manual/070A81050.pdf';
            AWG.obj = visadev(VisaAddr);
        end 
        
        function ClearDevice(AWG)
            AWG.writeline('CLS');
        end 
        
        function FlushDevice(AWG)
            AWG.flush()
        end 
        
        
        function GetInfo(AWG)
            tmp = query(AWG.obj, '*IDN?');
            disp(tmp)
        end 
        
        function SendData(AWG)
            
        end 
        
    end 
end
            
            