import pandas as pd

class Atab:
    """
    This class implements support for atab files.
    
    Input parameter:
    
    file: Input file
    sep : Separator for data (default: ';')
    
    Returns:
    
    nothing, but following data methods can be called on the object:
    
    header:  dictionary of header information of the atab file
    data  :  pandas DataFrame containing the data part of the atab file
    
    """
    def __init__(self,file,sep=";"):
        # consistency checks
        supported_seps = [" ",";"]
        if not sep in supported_seps:
            raise RuntimeError("Separator "+sep+" not supported. Must be one of "+",".join(supported_seps))

        # set instance variables
        self.file=file
        self.sep=sep
        self.n_header_lines=0
        self.header={}

        # parse file content
        self.data=None
        self._parse()



    def _parse(self):
        """
        This method parses the atab file.

        First, the header is parsed, then the remaining data block
        is parsed using panda's read_csv method.
        """
        # ============================
        # parse the header information
        # ============================
        self._parse_header()

        # ====================================================
        # parse the data section using panda's read_csv method
        # ====================================================
        # prepare arguments
        args = {"skiprows":self.n_header_lines,"parse_dates":True}
        if self.sep == " ":
            args["delim_whitespace"]=True
        else:
            args["sep"]=self.sep

        # call read_csv method
        self.data=pd.read_csv(self.file,**args)

        # ==========================================================
        # add experiment number as new column if available in header
        # ==========================================================
        experiment = self.header.get("Experiment",None)
        if experiment is not None:
            # number of rows
            n = len(self.data.index)
            # array of experiment numbers
            string_array = [experiment[0] for x in range(n)]
            # add column with experiment number
            self.data["Experiment"]=pd.Series(string_array,index=self.data.index)
            
        # ==========================================================
        # add product type as new column if available in header
        # ==========================================================
        product_type = self.header.get("Type_of_product",None)
        if product_type is not None:
            # number of rows
            n = len(self.data.index)
            # array of product_type numbers
            string_array = [product_type[0] for x in range(n)]
            # add column with product_type number
            self.data["Product_Type"]=pd.Series(string_array,index=self.data.index)

        # ===========================
        # remove columns with all NaN
        # ===========================
        self.data = self.data.dropna(axis=1,how="all")

        
    def _parse_header(self):
        """
        This method parses the header of the atab file.
        """
       
        # open file and read lines to list
        with open(self.file,"r") as f:
            lines = f.readlines()
        

        # loop over lines
        i=0
        while len(lines) > 0:

            # fetch line from the lines list
            line = lines.pop(0)

            # convert line to a list, split at ":"
            a = line.strip().split(':')

            # treat first line separately
            if i == 0:
                # extract format from header (ATAB odr XLS_TABLE)
                self.header["Format"]=a[0].strip(self.sep)
                line = lines.pop(0)
                i=i+1
                continue

            # stop extraction of header information if
            # no ':' was found in the line
            if (len(a)==1):
                self.n_header_lines = i+1
                break

            # add header information to dictionary
            # a list is generated by splitting at the separator
            key=a[0]
            self.header[key]="".join(a[1:]).strip(self.sep).split(self.sep)
            i=i+1
            
        # # check if all mandatory keys are in the header
        # extract header of the atab file and generate dictionary 
        # mandatory_keys=[
        #    "Width_of_text_label_column",
        #    "Number_of_integer_label_columns",
        #    "Number_of_real_label_columns",
        #    "Number_of_data_columns",
        #    "Number_of_data_rows",
        #    ]
        # key_set = set(list(self.header.keys()))    
        # print(self.header)
        # mandatory_key_set = set(mandatory_keys)
        # diff_set = mandatory_key_set - key_set
        # if len(diff_set):
        #     raise RuntimeError("Missing mandatory key(s) in header of "+self.file+": "+repr(diff_set))
