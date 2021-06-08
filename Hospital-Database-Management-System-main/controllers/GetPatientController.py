import peewee
import MySQLdb
from databases.Hospital_Database import PatTable,PatData,TestData
from datetime import date
from FormValidator import *

#get the patient record by Regno from Pattable & PatData
def getPatientRecords(regnNo):
        patDetails = None
        patData = None
        testData = None
        if PatTable.select().where(PatTable.regnNo == regnNo).exists():
                patDetails = PatTable.get(regnNo = regnNo)
                if PatData.select().where(PatData.regnNo == regnNo).order_by(-PatData.currentUnixTime).exists():
                        patData = PatData.select().where(PatData.regnNo == regnNo).order_by(-PatData.currentUnixTime)
                        if TestData.select().where(TestData.regnNo == regnNo).order_by(-TestData.currentUnixTime).exists():
                                testData = TestData.select().where(TestData.regnNo == regnNo).order_by(-TestData.currentUnixTime)
        return patDetails, patData, testData

#get all the patient records with the same name from PatTable
def getAllRecordsByName(patientName):
        patients = None
        if PatTable.select().where(PatTable.name == patientName).exists():
                patients = PatTable.select().where(PatTable.name == patientName)
        return patients

#get all test records of patient between start date and end date
def getAllPatientRecordsByDate(startDate,endDate):
        patientRecords = None
        if len(PatData.select(PatData.regnNo).where(PatData.dataOfVisit > startDate,PatData.dataOfVisit < endDate)) != 0:
                patientRecords = PatData.select(PatTable.name,PatTable.regnNo,PatData.dataOfVisit).join(PatTable).where(PatData.dataOfVisit > startDate, PatData.dataOfVisit < endDate)
        return patientRecords
        
def getPatientTest(regnNo,dateOfVisit):
	if dateOfVisit != None:
		testDataDetails = TestData.select().where(
                        TestData.regnNo == regnNo,
                        TestData.testDate == dateOfVisit
                )
	else:
		testDataDetails = TestData.select().where(TestData.regnNo == regnNo)
	print testDataDetails[0].testName
	
#get all patients [name,diagnosis] for the given date (query by NextDateOfVisit)
def getPatientsByDate(date = str(date.today())):
        patients = None
        if PatData.select().where(PatData.nextDateOfVisit == date).exists():
                patients = PatData.select(PatTable.regnNo,PatTable.name,PatData.diagnosis).join(PatTable).where(PatData.nextDateOfVisit == date)
        return patients
        
