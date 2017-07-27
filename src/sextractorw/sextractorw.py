from __future__ import print_function
import os
import sys
import tempfile
import copy
import subprocess

class SExtractorW:
    """Low level SExtractor wrapper."""
    
    def __init__(self, config_file='', output_params=[], sexpath='sex',
            **kwargs):
        """
        Configure SExtractor. Settings here will be passed to all SExtractor
        calls unless overridden.

        Arguments:
            config_file (str): SExtractor configuration file
            output_params (:obj:`list` of :obj:`str`): Output catalog columns
            sexpath (str): SExtractor executable location
            **kwargs: Additional parameters passed directly to SExtractor

        Note:
            output_params will override the param file in config_file.

        Note:
            PARAMETERS_NAME, FILTER_NAME and STARNNW_NAME must all be valid if
            a config_file is supplied.
        """
        self.output_params = output_params
        self.sexpath = sexpath
        self.kwconfig = kwargs

        module_dir = os.path.dirname(sys.modules[__name__].__file__)
        self.config_dir = os.path.join(module_dir, 'config')

        if config_file:
            self.config_file = config_file
        else:
            self.config_file = os.path.join(self.config_dir, 'default.sex')

            # nnw file never needs to be changed
            nnw_file = os.path.join(self.config_dir, 'default.nnw')
            self.kwconfig.update({'STARNNW_NAME': nnw_file})

            # set location of default.conv if used
            if 'FILTER_NAME' not in kwargs:
                filter_name = os.path.join(self.config_dir, 'default.conv')
                self.kwconfig.update({'FILTER_NAME': filter_name})

            # more sensible memory defaults
            if 'MEMORY_OBJSTACK' not in kwargs:
                self.kwconfig.update({'MEMORY_OBJSTACK': 30000})
            if 'MEMORY_PIXSTACK' not in kwargs:
                self.kwconfig.update({'MEMORY_PIXSTACK': 300000})
            if 'MEMORY_BUFSIZE' not in kwargs:
                self.kwconfig.update({'MEMORY_BUFSIZE': 30000})


    def _create_outparams_file(self, output_params):
        """
        Create tmpfile holding output catalog columns.

        Arguments:
            output_params (:obj:`list` of :obj:`str`): Output catalog columns
        """
        outparams_contents = '\n'.join(output_params)
        # creating instance variable delays garbage collection so tmpfile is
        # not deleted
        self._outparams_fp = tempfile.NamedTemporaryFile(bufsize=0)
        self._outparams_fp.write(outparams_contents)
        return self._outparams_fp.name


    def run(self, image, output_params=[], **kwargs):
        """
        Run SExtractor.
        
        Arguments:
            image (str): FITS image
            output_params (:obj:`list` of :obj:`str`): Output catalog columns
            **kwargs: additional parameters passed directly to SExtractor

        Note:
            output_params overrides self.output_params.

        Note:
            **kwargs passed here are not saved.
        """
        run_params = copy.deepcopy(self.kwconfig)
        run_params.update(kwargs)

        # create tmpfile holding list of output parameters, if given
        if not output_params:
            output_params = self.output_params
        if output_params:
            outparams_name = self._create_outparams_file(output_params)
            run_params.update({'PARAMETERS_NAME': outparams_name})

        # try and find filter
        if 'FILTER_NAME' in run_params and not os.path.exists(run_params['FILTER_NAME']):
            filter_name = os.path.join(self.config_dir, run_params['FILTER_NAME'])
            run_params.update({'FILTER_NAME': filter_name})

        command = [self.sexpath, '-c', self.config_file, image]
        for kw in run_params:
            command.extend(['-'+str(kw), str(run_params[kw]).replace(' ', '')])
        return subprocess.call(command)


    def dualimagemode(self, detect, measure, detect_weight='',
            measure_weight='', output_params=[], **kwargs):
        """
        Run SExtractor in dual-image mode.

        Arguments:
            detect (str): Detection image
            measure (str): Measurement image
            detect_weight (str): Detection weight image
            measure_weight (str): Measurement weight image
            output_params (:obj:`list` of :obj:`str`): Output catalog columns
            **kwargs: Additional parameters passed directly to SExtractor

        Note:
            detect_weight and measure_weight, if present, will override
            WEIGHT_IMAGE in **kwargs

        Note:
            output_params overrides self.output_params.

        Note:
            **kwargs passed here are not saved.
        """
        weight_image = ','.join([detect_weight, measure_weight])
        if weight_image != ',':
            kwargs.update({'WEIGHT_IMAGE': weight_image})

        image = ','.join([detect, measure])

        return self.run(image, output_params, **kwargs)
