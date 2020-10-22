function sheets = getSheetNames(filename)
% SHEETNAMES(FILENAME) returns the sheet names from the given spreadsheet FILENAME
%   FILENAME: If the file is not on the MATLAB path, you must specify the
%   full path to the file on the local machine or as an URL for a remote file
%
%   Example:
%   --------
%   sheets = sheetnames('testData.xlsx');% File is on MATLAB path
%   sheets = sheetnames('C:\Users\username\Desktop\testData.xlsx'); % Absolute path to file
%   sheets = sheetnames('s3://bucketname/path_to_file'); % Remote s3 file

% Copyright 2018-2019 The MathWorks, Inc.

import matlab.io.spreadsheet.internal.*;

if ~matlab.internal.datatypes.isScalarText(filename)
    error('sheetnames:InputMustBeScalar','Filename must be a non-empty character vector or string scalar.');
end

try
    filename = convertStringsToChars(filename);

    validFilename = matlab.io.internal.validators.validateFileName(filename);
    filename = validFilename{1};

    
    ext = getExtension(filename);
    bookObj = createWorkbook(ext, filename, false);
    sheets = bookObj.SheetNames;
catch ME
    if strcmp(ME.identifier, 'MATLAB:spreadsheet:book:fileTypeUnsupported')
        error(message('MATLAB:spreadsheet:book:invalidFormatUnix'));
    end
    throw(ME);
end
end
