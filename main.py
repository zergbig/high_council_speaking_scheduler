import sys
import random
import inspect


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def log(*args, **kwargs):
    frames = inspect.getouterframes(inspect.currentframe())
    frameinfo = inspect.getframeinfo(sys._getframe().f_back)
    print(sys._getframe().f_back.f_code.co_name, ':', frameinfo.lineno, ' - ', *args, **kwargs, sep='')


class Assignment:
    def __init__(self, date, ward, hc, comp):
        self.date = date
        self.ward = ward
        self.hc = hc
        self.companion = comp

    def __str__(self):
        return 'Assignment - Date: ' + self.date + ', Ward: ' + self.ward + ', HC: ' + self.hc.name + \
               ', Comp: ' + self.companion.name + ']'

    def __eq__(self, other):
        return self.date == other.date and self.ward == other.word


class HC:
    def __init__(self, name, home_ward):
        self.name = name
        self.home_ward = home_ward
        self.MAX_SPEAKING_ASSIGNMENTS = 7
        self.assignments = []
        self.wards = []
        self.dates = []

    def __str__(self):
        return self.name + ', num_speaking_assignments: ' + str(len(self.assignments)) + ', home_ward: ' + \
               self.home_ward + '\n\t' + ',\n\t'.join(str(a) for a in self.assignments)

    def add_hc_speaking_assignment(self, assignment):
        if len(self.assignments) >= self.MAX_SPEAKING_ASSIGNMENTS:
            log('Too many assignments for ', self.name, ', not adding ', assignment)
            return False
        elif assignment.ward in self.wards:
            log('Cannot add assignment, HC ', self.name, ' is already speaking in ward ', assignment.ward)
            return False
        elif assignment.date in self.dates:
            log('Tried to add assignment for same date: ', assignment.date)
            return False
        else:
            self.assignments.append(assignment)
            self.wards.append(assignment.ward)
            self.dates.append(assignment.date)

        return True


class Companion:
    def __init__(self, name, max_assignments, home_ward, ignore_restrictions=False):
        self.name = name
        self.max_assignments = max_assignments
        self.home_ward = home_ward
        self.assignments = []
        self.wards = []
        self.dates = []
        self.hcs = []
        self.ignore_restrictions = ignore_restrictions
        self.next_allowed_date = None

    def __str__(self):
        return 'Companion: ' + self.name + ', home_ward: ' + self.home_ward + ', num_assignments: ' + \
               str(len(self.assignments)) + ', max_assignments: ' + \
               str(self.max_assignments) + '\n\tHCs: ' + ', '.join(str(hc.name) for hc in self.hcs) + \
               '\n\tDates: ' + ', '.join(d for d in self.dates)

    def add_comp_speaking_assignment(self, assignment):
        if not self.ignore_restrictions and assignment.hc in self.hcs:
            log('Tried to add assignment for exiting high councilor: ', assignment.hc)
            return False
        elif len(self.hcs) >= self.max_assignments:
            log('Too many speaking dates: ', len(self.hcs), ', not adding "', assignment.hc.name, '" to ', self.name)
            return False
        elif assignment.ward is self.home_ward:
            log('Tried to add assignment for home ward: ', self.home_ward)
            return False
        elif not self.ignore_restrictions and assignment.ward in self.wards:
            log('Tried to add assignment for existing ward')
            return False
        elif not self.ignore_restrictions and assignment.date in self.dates:
            log('Tried to add assignment for exiting speaking date: ', assignment.date)
            return False
        else:
            # log('Adding HC: ', assignment.hc.name, ' to ', self.name)
            self.assignments.append(assignment)
            self.wards.append(assignment.ward)
            self.dates.append(assignment.date)
            self.hcs.append(assignment.hc)

        return True


def find_high_councilor(date, adult_speaker_months, high_councilors, ward, allow_home_ward):
    # Things to check:
    # - if he has spoken on that date
    # - if he has spoken in that ward
    # - if he has not yet spoken 7 times
    # - Not allowed to speak in home ward
    # - Don't let Brother Howarth speak in months where the ward will provide an adult speaker
    for i in range(len(high_councilors)):
        hc = random.choice(high_councilors)
        high_councilors.remove(hc)
        if hc.name == howarth_name and date in adult_speaker_months:
            continue
        elif date in hc.dates:
            continue
        elif ward in hc.wards:
            continue
        elif len(hc.dates) >= hc.MAX_SPEAKING_ASSIGNMENTS:
            continue
        elif not allow_home_ward and hc.home_ward is ward:
            continue
        else:
            return hc

    log('Did not find a high councillor for ', ward, ' ward on ', date)
    return None


def find_companion(date, date_index, ward, high_councilor, companions, copy_companions=True):
    # Things to check:
    # - if he has spoken on that date
    # - if he has spoken in that ward
    # - if he has spoken with that HC
    # - if he has not yet spoken MAX times
    # - Not allowed to speak in home ward
    if copy_companions:
        comps = companions.copy()
    else:
        comps = companions

    for j in range(len(comps)):
        comp = random.choice(comps)
        comps.remove(comp)
        if not comp.ignore_restrictions and date in comp.dates:
            continue
        elif not comp.ignore_restrictions and ward in comp.wards:
            continue
        elif len(comp.dates) >= comp.max_assignments:
            continue
        elif not comp.ignore_restrictions and comp.home_ward is ward:
            continue
        elif not comp.ignore_restrictions and high_councilor in comp.hcs:
            continue
        elif comp.next_allowed_date is not None and comp.next_allowed_date > date_index:
            continue
        else:
            return comp

    log('Did not find a companion for ', ward, ' ward on ', date, ' with ', high_councilor)
    return None


def print_assignments(assignments):
    for a in assignments:
        log(a)


def main():
    random.seed()
    assignments = []
    dates = ['February', 'March', 'April', 'May', 'July', 'August', 'September', 'October', 'November', 'December']
    adult_speaker_months = [dates[0], dates[6]]
    #         0      1      2      3      4      5      6      7
    wards = ['1st', '3rd', '4th', '5th', '6th', '7th', '8th', '9th']
    high_councilors = [HC('Booth', wards[2]), HC("P Johnson", wards[0]), HC('Padilla', wards[1]),
                       HC('Nielsen', wards[5]), HC('Hammond', wards[0]), HC('R Johnson', wards[1]),
                       HC('Diamond', wards[2]), HC('Ekberg', wards[3]), HC('Pope', wards[4]),
                       HC('Bascom', wards[6]), HC(howarth_name, wards[4]), HC('Hemsath', wards[3])]

    companions_that_speak_twice = [Companion('RS Pres - Rebecca Lowell', 2, wards[4]),
                                   Companion('RS 1st - Roxine Hodson', 2, wards[0]),
                                   Companion('RS 2nd - Shayla Christofferson', 2, wards[5]),
                                   Companion('RS Sec - Terri Klug', 2, wards[6]),
                                   Companion('YW Pres - Joy Edmand', 2, wards[2]),
                                   Companion('YW 1st - Jill Christensen', 2, wards[3]),
                                   Companion('YW 2nd - Mandy Spencer', 2, wards[4]),
                                   Companion('YW Sec - Julie Reynolds', 2, wards[1]),
                                   Companion('Primary Pres - Megan Powell', 2, wards[0]),
                                   Companion('Primary 1st - Julia Pearce', 2, wards[6]),
                                   Companion('Primary 2nd - Julie Petersen', 2, wards[5]),
                                   Companion('Primary Sec - Margaret Hess', 2, wards[2]),
                                   Companion('Primary - Music Leader', 2, wards[1]),
                                   Companion('YM 1st - Rick Carlson', 2, wards[1]),
                                   Companion('YM 2nd - Adam Derfler', 2, wards[2]),
                                   # Companion('YM Sec - ', 2, wards[]),
                                   Companion('SS 1st - Jeremy Christensen', 2, wards[2]),
                                   # Companion('SS 2nd - TBD', 2, wards[]),
                                   # Companion('SS Sec - TBD', 2, wards[]),
                                   ]

    companions_all = [#Companion('Stake Clerk - David Vandenberg', 1, wards[5]),
                      #Companion('Stake Exec Sec - Karl Zeibig', 1, wards[7]),
                      Companion('Stake Pres 2nd - Lance Pearson', 2, wards[7]),
                      Companion('Self-Reliance - Dalen Slater', 1, wards[0]),
                      Companion('Temple & FH - Whitney Cox', 1, wards[0]),
                      Companion('Temple & FH - Luana Darby', 1, wards[6]),
                      Companion('Temple & FH - Clint Melander', 1, wards[2]),
                      Companion('Stake Music Coordinator - Annalee Munsey', 1, wards[0]),
                      Companion('Stake Pres 1st - Darin Dickson', 1, wards[0])
    ]
    companions_all.extend(companions_that_speak_twice)

    # Addd Ward Mission Leaders for Brother Howarth
    ward_mission_leader = Companion('Ward Mission Leader', 7, 'Any Ward', True)

    # Only 15 RMs come home between Jan and Nov in 2022 that could speak. Unsure if the ones coming home in
    # July and August will be available to speak in Sept due to possible school

    # 3 RMs in Dec that could speak

    # 2 RMs in Jan that could speak in Feb
    # No RMs are needed in Feb since it is an Adult Speaker month
    # rms_feb = [Companion('RM Jan 1', 1, 'No Ward'),
    #           Companion('RM Jan 2', 1, 'No Ward')]

    # 2 RMs in Jan and 1 in Feb that could speak in Mar
    rms_mar = [Companion('RM Feb 1', 1, 'No Ward'),
               Companion('RM Jan 1', 1, 'No Ward'),
               Companion('RM Jan 2', 1, 'No Ward')]

    # 1 RM in Feb and 1 in Mar that could speak in Apr
    rms_apr = [Companion('RM Mar 1', 1, 'No Ward'),
               Companion('RM Feb 1', 1, 'No Ward')]

    # 1 RM in Mar and 2 RM in Apr that could speak in May
    rms_may = [Companion('RM Apr 1', 1, 'No Ward'),
               Companion('RM Apr 2', 1, 'No Ward'),
               Companion('RM Mar 1', 1, 'No Ward')]

    # 2 RM in May that could speak in July
    rms_jul = [Companion('RM May 1', 1, 'No Ward'),
               Companion('RM May 2', 1, 'No Ward')]

    # 2 RM in July that could speak in August
    rms_aug = [Companion('RM Jul 1', 1, 'No Ward'),
               Companion('RM Jul 2', 1, 'No Ward')]

    # rm_sep = Companion('RM Sep', 2, 'HNoome Ward')  # No RMs
    # rm_oct = Companion('RM Oct', 2, 'No Ward')  # No RMs

    # 2 RM in Oct that could speak in Nov
    rms_nov = [Companion('RM Oct 1', 1, 'No Ward'),
               Companion('RM Oct 2', 1, 'No Ward'), ]

    # 3 RM in Nov that could speak in Dec
    rms_dec = [Companion('RM Nov 1', 1, 'No Ward'),
               Companion('RM Nov 2', 1, 'No Ward'),
               Companion('RM Nov 3', 1, 'No Ward')]

    ward_adult_speaker = Companion('Ward Adult Speaker', 16, 'Home Ward', True)

    for date in dates:
        wards_copy = wards.copy()
        for i in range(len(wards_copy)):
            ward = random.choice(wards_copy)
            wards_copy.remove(ward)
            # Find HC
            # Things to check:
            # - if he has spoken on that date
            # - if he has spoken in that ward
            # - if he has not yet spokent 7 times
            # - Not allowed to speak in home ward
            hc = find_high_councilor(date, adult_speaker_months, high_councilors.copy(), ward, False)
            if hc is None:
                hc = find_high_councilor(date, adult_speaker_months, high_councilors.copy(), ward, True)

            if hc is None:
                # There is a problem, we should have found a high councilor
                # print_assignments(assignments)
                for h in high_councilors:
                    log(h)
                log('ERROR: Could not find a high councilor for ', ward, ' ward on ', date, '. Cannot continue!')
                return 1

            #           0           1        2        3      4       5         6            7          8           9
            # dates = ['February', 'March', 'April', 'May', 'July', 'August', 'September', 'October', 'November', 'December']

            # In February and September we use Ward Adult Speakers
            if date is dates[0] or date is dates[6]:
                comp = ward_adult_speaker
            elif howarth_name is hc.name:
                comp = ward_mission_leader
            else:
                # Use RMs before Stake Leaders
                if date is dates[1] and len(rms_mar) > 0:  # March
                    comp = find_companion(date, dates.index(date), ward, hc, rms_mar, False)

                elif date is dates[2] and len(rms_apr) > 0:  # April
                    comp = find_companion(date, dates.index(date), ward, hc, rms_apr, False)

                elif date is dates[3] and len(rms_may) > 0:  # May
                    comp = find_companion(date, dates.index(date), ward, hc, rms_may, False)

                elif date is dates[4] and len(rms_jul) > 0:  # July
                    comp = find_companion(date, dates.index(date), ward, hc, rms_jul, False)

                elif date is dates[5] and len(rms_aug) > 0:  # August
                    comp = find_companion(date, dates.index(date), ward, hc, rms_aug, False)

                elif date is dates[8] and len(rms_nov) > 0:  # November
                    comp = find_companion(date, dates.index(date), ward, hc, rms_nov, False)

                elif date is dates[9] and len(rms_dec) > 0:  # December
                    comp = find_companion(date, dates.index(date), ward, hc, rms_dec, False)

                elif len(companions_that_speak_twice) > 0:
                    comp = find_companion(date, dates.index(date), ward, hc, companions_that_speak_twice)
                    if comp is not None:
                        comp.next_allowed_date = dates.index(date) + 4
                        companions_that_speak_twice.remove(comp)
                    else:
                        log('ERROR - Did not find companion speaker from companions that speak twice, len is ',
                            len(companions_that_speak_twice))

                else:
                    comp = find_companion(date, dates.index(date), ward, hc, companions_all)

                if comp is None:
                    # There is a problem, we should have found a companion

                    # print_assignments(assignments)
                    print('\n\n')
                    for c in companions_all:
                        log(c)

                    print('\n')

                    log('ERROR: Could not find a companion for ', ward, ' ward on ', date, ' with ', hc.name)
                    return 2

            assignment = Assignment(date, ward, hc, comp)

            hc_added = hc.add_hc_speaking_assignment(assignment)
            if not hc_added:
                print_assignments(assignments)
                log('ERROR: Could not add assignment "', str(assignment), '" to high councilor ', str(hc))
                return 3

            comp_added = comp.add_comp_speaking_assignment(assignment)
            if not comp_added:
                print_assignments(assignments)
                log('ERROR: Could not add assignment "', str(assignment), '" to companion ', str(comp))
                log('ERROR: HC for assignment: ', assignment.hc)
                log('ERROR: Comp for assignment: ', assignment.companion)
                return 4

            assignments.append(assignment)

    print_assignments(assignments)
    print('\n\n')
    for c in companions_all:
        log(c)

    return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    howarth_name = 'Howarth'
    for i in range(100):
        rc = main()
        if rc == 0:
            break

    if rc == 0:
        print('\nCompleted on iteration', str(i), ':)')
    else:
        print('\nCould not complete in' , str(i), 'iterations')
