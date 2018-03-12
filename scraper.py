from importlib import reload
import pdfquery

import incident
reload(incident)
from incident import Incident
import timing
reload(timing)
import utils
reload(utils)
import glob

def get_text_from_curve(ltcurve):
    # text can be within LTTextBoxHorizontal or LTTextLineHorizontal
    # the problem is that these are interleaved
    # so we select EITHER as they come
    # if we chose the Boxes first and the Lines second then merged those lists,
    # the resulting list would be out of order!
    # e.g. if the true order is B1 L1 B2 B3 L2, the approach we are using
    # gives you the right order... but choosing Boxes and Lines separately
    # gives you B1 B2 B3 L1 L2!!!!
    textual_elements = ltcurve.cssselect("LTTextBoxHorizontal, LTTextLineHorizontal")
    texts = [t.text.strip() for t in textual_elements]

    # remove empty lines
    cleaned_texts = [t for t in texts if t != '']

    # PROBLEM with this approach: in rare cases some text from this falls way
    # outside the ltcurve. Might it still be within the bounding box though?

    # UPDATE: try gathering all data
    # for 11/28 consider these bboxes
    #
    # 10:08am [247.08, 80.197, 275.587, 90.18]
    # hp laptop [6.0, 65.784, 737.868, 82.318]
    # bounding box [3.36, 77.7, 754.86, 98.64]

    return cleaned_texts

def get_comments(pdf):
    # filtering function
    def comment_filter():
        return this.get('word_margin',0) == "0.1" and this.get('x0', 0) == "6.0" and this.get('x1', 0) == "737.868"

    comment_lines = pdf.pq('LTTextLineHorizontal').filter(comment_filter)

    def extract_text(comment_line):
        # sometimes text lives directly in the LTTextLine (which is passed),
        # sometimes it lives within a LTTextBox within the LTTextLine.
        # This standardizes that.
        if comment_line.text != '':
            # Contains text directly
            return comment_line.text
        else:
            text_box = comment_line.find("LTTextBoxHorizontal")

            if text_box is not None:
                # This is the Box inside the Line
                return text_box.text

            else:
                return None

    comments = [extract_text(line) for line in comment_lines]

    # Now smoosh the lines together. Lines beginning with
    # "Officer" are probably a new entry. Everything else
    # should be lumped with the previous line.

    cleaned_comments = []
    for comment in comments:
        if comment.startswith("Officer"):
            # proper new comment. add to the list!
            cleaned_comments.append(comment)
        else:
            # it's the next line of the previous comment.
            # add it to the previous comment.
            # these lines usually have spaces between them already
            # so no need to add a new one
            cleaned_comments[-1] += comment

    return cleaned_comments

def incidents_of_pdf(pdf):
    """
    Pass this function the result of a pdfquery.PDFQuery() function.
    This will read through the pdf file and return a list of
    Incident objects contained in there!

    Make sure the PDF is load()'ed before you pass it.
    """

    # TODO watch out for things like 11/24/17 where there were no incidents. there's a specific tag for those.

    # so each individual report, as well as headers, is filed inside
    # its own <LTCurve>. The text fields are inside <LTTextLineHorizontal>s and <LTTextBoxHorizontal>s
    # inside the <LTCurve>.
    reports_plus_heads = pdf.tree.findall(".//LTCurve")

    # extract raw incidents
    raw_incidents = [get_text_from_curve(lt) for lt in reports_plus_heads]

    # remove headers of tables
    HEADER_ROW_TEXT = ['Reported', 'Incident Type', 'Occurred', 'Location', 'Disposition']
    incidents_without_headers = [i for i in raw_incidents if i != HEADER_ROW_TEXT]

    # convert incidents to proper objects
    # 9 = proper length of report; anything less is malformed
    # TODO clean up — extract error checking into its own make_incident_objects() function
    incident_objects = [incident.Incident(i) for i in incidents_without_headers if len(i) == 9]

    # get the comments from this pdf
    comments = get_comments(pdf)
    # there should be as many comments as incidents, so attach one to each
    # (in order)
    if len(comments) == len(incident_objects):
        for i in range(0, len(comments)):
            incident_objects[i].comments = comments[i]
    else:
        # PROBLEM: if the number of comments != the number of incidents,
        # we currently don't attach any comments to anyone.
        # is there a way to match comments individually to incidents
        # (like the LTCurves)? perhaps by x/y coords? that might help
        print("Wrong length comments!")
        print(comments)
        print(len(comments))
        print(incident_objects)
        print(len(incident_objects))

    return incident_objects

# Go through new pdfs in our data folder

def scrapeNew(fileNames):
    all_incidents = []

    for filename in fileNames:
        # filename will be like `data/xxxxxx.pdf`
        # extract incidents from this file
        pdf = pdfquery.PDFQuery("%s.pdf" % filename)
        pdf.load()
        new_incidents = incidents_of_pdf(pdf)
        all_incidents += new_incidents

        print("Done {}".format(filename))

    # dump to csv
    utils.dump_csv(all_incidents)
    print("Dumped!")
