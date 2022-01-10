classdef Tektronix_AWG610
    % driver for Tektronix AWG 610 arbitrary waveform generator
    % Developed by Daniel Hutama
    % Version 0.2 10 Jan 2022
    % visadev needs Matlab R2021a or newer to work.
    
    % This device uses IEEE 488.2 
    % Standard Commands for Programmable Instruments (SCPI) 
    

        
    properties
        obj
        model
        gpib_addr
        info
        manualURL
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
            configureTerminator(AWG.obj, "LF", "LF")
        end 

        function GetInfo(AWG)
            tmp = writeread(AWG.obj, '*IDN?');
            disp(tmp)
        end 
        
        function GetRunState(AWG)
            tmp = writeread(AWG.obj, 'AWGC:RST?');
            disp(tmp)
        end 

        function GetAmplitude(AWG)
            tmp = writeread(AWG.obj, 'SOUR:VOLT:AMPL?');
            disp(tmp)
        end 

        function SetAmplitude(AWG, amplitude)
            writeline(AWG.obj, strcat("SOUR:VOLT:AMPL ", string(amplitude)));
            GetAmplitude(AWG)
        end     

        function GetFrequency(AWG)
            tmp = writeread(AWG.obj, "SOUR:FREQ:CW?");
            disp(tmp)
        end 

        function SetFrequency(AWG, freq) %enter frequency in megahertz
            writeline(AWG.obj, strcat("SOUR:FREQ:CW ", string(freq), " mhz"))
            GetFrequency(AWG)
        end 

        function GetOutputState(AWG)
            tmp = writeread(AWG.obj, "OUTP:STAT?");
            disp(tmp)
        end 

        function SetOutputState(AWG, state)
            writeline(AWG.obj, strcat("OUTP:STAT ", string(state)))
            GetOutputState(AWG)
        end 

        function GetLowPassFilterFrequency(AWG)
            tmp = writeread(AWG.obj, "OUTP:FILT:LPAS:FREQ?");
            disp(tmp)
        end 

        function SetLowPassFilterFrequency(AWG, freq) %enter low pass cutoff frequency in Mhz
            options = [20e6, 50e6, 100e6, 200e6, 9.9e37];
            %needs to be in options list
            writeline(AWG.obj, strcat("OUTP:FILT:LPAS:FREQ ", string(freq)))
            GetLowPassFilterFrequency(AWG)
        end 

        function GetCustomWaveform(AWG)
            tmp = writeread(AWG.obj, "SOUR:FUNC:USER?");
            disp(tmp)
        end 

        function SetCustomWaveform(AWG, filename)
            mystring = "SOUR:FUNC:USER ""%s "", ""MAIN"" ";
            writeline(AWG.obj, sprintf(mystring, filename))
            GetCustomWaveform(AWG)
        end 

        function GetReferenceOscillator(AWG)
            tmp = writeread(AWG.obj, "SOUR:ROSC:SOUR?");
            disp(tmp)
        end 
         
        function SetReferenceOscillator(AWG, ref) %either EXT or INT
            writeline(AWG.obj, strcat("SOUR:ROSC:SOUR ",ref))
            GetReferenceOscillator(AWG)
        end 
        
        function GetVoltageOffsetDC(AWG) %number in mV between -1000 and +1000 mV
            tmp = writeread(AWG.obj, "SOUR:VOLT:LEV:IMM:OFFS?");
            disp(tmp)
        end 

        function SetVoltageOffsetDC(AWG, offset)
            writeline(AWG.obj, strcat("SOUR:VOLT:LEV:IMM:OFFS ", string(offset), "mV"))
            GetVoltageOffsetDC(AWG)
        end 
    
        function ResetAWG(AWG)
            writeline(AWG.obj, "*RST")
            disp("AWG has been reset.")
        end 

        function SetForceTrigger(AWG)
            writeline(AWG.obj, "*TRG")
            disp("Trigger has been force-set.")
        end 

        function GetTrigImpedance(AWG) %either 50 (ohm) or 1e3 (kOhm)
            tmp = writeread(AWG.obj, "TRIG:SEQ:IMP?");
            disp(tmp)
        end 

        function SetTrigImpedance(AWG, impedance)
            writeline(AWG.obj, strcat("TRIG:SEQ:IMP ", string(impedance)))
            GetTrigImpedance(AWG)
        end

        function GetTrigLevel(AWG)
            tmp = writeread(AWG.obj, "TRIG:SEQ:LEV?");
            disp(tmp)
        end 

        function SetTrigLevel(AWG, level) % enter in mV between -5 V and +5 V in 0.1V steps
            writeline(AWG.obj, strcat("TRIG:SEQ:LEV ", string(level*1000), "mV"))
            GetTrigLevel(AWG)
        end 
        
        function GetTrigPolarity(AWG)
            tmp = writeread(AWG.obj, "TRIG:POL?");
            disp(tmp)
        end 

        function SetTrigPolarity(AWG, polarity) %either POS or NEG
            writeline(AWG.obj, strcat("TRIG:POL ", polarity))
            GetTrigPolarity(AWG)
        end 

        function GetTrigSlope(AWG)
            tmp = writeread(AWG.obj, "TRIG:SLOP?");
            disp(tmp)
        end 

        function SetTrigSlope(AWG, slope) %POS means rising edge trigger, NEG means falling edge trigger
            writeline(AWG.obj, strcat("TRIG:SLOP ", slope))
            GetTrigSlope(AWG)
        end 

        function GetTrigSource(AWG)
            tmp = writeread(AWG.obj, "TRIG:SEQ:SOUR?");
            disp(tmp)
        end 

        function SetTrigSource(AWG, source) %either INT or EXT
            writeline(AWG.obj, strcat("TRIG:SEQ:SOUR ", source))
            GetTrigSource(AWG)
        end 

        function GrabScreen(AWG, filename) %filename ending with .BMP
            writeline(AWG.obj, strcat("MMEM:NAME ", """", filename, """;:HCOP:SDUM:IMM"))
            disp('File has been saved.')
        end 

        function GetFileList(AWG)
            tmp = writeread(AWG.obj,"MMEM:CAT? ""MAIN""");
            disp(tmp)
        end 

        function CopyFile(AWG, filename, copyname)
            writeline(AWG.obj, strcat("MMEM:COPY ", """", filename, """", ", ""MAIN"",", """", copyname, """", ", ""MAIN""" ))
        end 

        function LoadFile(AWG, filename)
            writeline(AWG.obj, strcat("MMEM:DATA """, filename, """"))
        end 

        function DeleteFile(AWG, filename)
            writeline(AWG.obj, strcat("MMEM:DEL """, filename, """"))
        end 


    end 
end
            
            