import os
import re
from tqdm import tqdm
from .patient import Patient
from config import config

from multiprocessing import Pool

class PatientGroup:
    """
    Data housing for a patient category
    """

    def __init__(self, path: str, load_other=False):
        """
        :param bool load_other: Load all exercises except the predefined ones
        """

        self.path = path
        self.patients = list()
        self.id = int(re.findall(r'_(\d+)', path)[0])
        self.__generate_patients_list(load_other)
    
    def get_patient(self, patient_id):
        """
        Get the patient with the given id from the list

        :param int patient_id: patient id to lookup
        :return: Patient object
        :rtype: Patient
        :raise: ValueError
        """
        for pat in self:
            if pat.id == patient_id:
                return pat

        raise ValueError("Patient %i does not exist in this collection (%i)" % (patient_id, self.id))
    
    @staticmethod
    def make_patient_object(args):
        return Patient(*args)

    def __generate_patients_list(self, load_other: bool):
        """
        Generate patients list
        :param bool load_other: Load all exercises except the predefined ones
        """
        if not os.path.exists(self.path):
            # TODO: Indicate to the user a path is skipped
            raise FileNotFoundError("Folder does not exists")
        
        if config.multithreading: 
            patient_paths = []
            # Looping through files in patient folder
            for name in os.listdir(self.path):
                patient_path = os.path.join(self.path, name)
                if os.path.isdir(patient_path):
                    patient_paths.append([patient_path, load_other])

            pool = Pool(config.workers) 
            path_count = len(patient_paths) 
            for _ in tqdm(pool.imap_unordered(PatientGroup.make_patient_object, patient_paths), total=path_count):
                pass

            self.patients = pool.map(PatientGroup.make_patient_object, patient_paths)
        else: 
            for name in tqdm(os.listdir(self.path), desc=" Patientgroup {id}".format(id=self.id)):
                patient_path = os.path.join(self.path, name)
                if os.path.isdir(patient_path):
                    self.patients.append(Patient(patient_path, load_other))

    def __iter__(self):
        self._index = -1
        return self

    def __next__(self):
        if self._index < len(self.patients) - 1:
            self._index += 1
            return self.patients[self._index]

        raise StopIteration

    def __str__(self):
        _patients = str()
        for p in self.patients:
            _pat = re.findall(r'/(\d+)', p.path)[0]
            _patients += _pat + ","
        _patients = _patients[:-1]

        return "Patientgroup\n"\
            "------------\n"\
            "Path: %s\n"\
            "Patients: %s" % (self.path, _patients)
