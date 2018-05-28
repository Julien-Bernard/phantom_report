#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# __author__ = 'julien.bernard <julien.bernard@gmail.com>'
# __description__ = 'Python script to create a timeline PDF report from Phantom.us'

"""
This scripts creates a PDF report for a specific Phantom container
"""

import config as cfg
import argparse
import logging
import json
import requests
from weasyprint import HTML,CSS


"""
Logging configuration
"""
logging_level = cfg.LOGGING_LEVEL
logging.basicConfig(format='# %(levelname)10s:\t%(message)s', level=logging_level)


""" main() """
def main():
    """Primary entry point"""

    """Getting arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("containerID", help="Phantom container ID")
    parser.add_argument("output", help="Output filename (.pdf)")
    args = parser.parse_args()

    container_id = args.containerID
    filename = args.output
    
    """Collecting information"""
    logging.debug('Calling "get_details" for container function')
    container = get_details(cfg.PHANTOM_SERVER, cfg.PHANTOM_TOKEN, container_id, "container")
    logging.debug('Calling "get_details" for comments function')
    comments = get_details(cfg.PHANTOM_SERVER, cfg.PHANTOM_TOKEN, container_id, "comments")
    logging.debug('Calling "get_details" for phases function')
    phases = get_details(cfg.PHANTOM_SERVER, cfg.PHANTOM_TOKEN, container_id, "phases")
    logging.debug('Calling "get_details" for notes function')
    notes = get_details(cfg.PHANTOM_SERVER, cfg.PHANTOM_TOKEN, container_id, "notes")

    """Report creation"""
    try:
        # STYLESHEET
        stylsheet = """
			@page
			{{   
                size: letter;
				margin: 15mm 15mm 15mm 15mm;
				padding-top: 10mm;
				counter-increment: page;

				@top-left {{
                        content: "{0}";
						font-size: 1.4em;
                        padding: 0.5em 0;
                        border-bottom: 1px solid #aaa;
                        vertical-align: bottom;
                        width: 100%;
				}}
				
				@bottom-left {{
						border-top: 1px solid #aaa;
						content: "{1}";
						font-size: 0.8em;
						padding: 0.5em 0;
						vertical-align: top;
						width: 100%;
				}}

				@bottom-right {{
						border-top: 1px solid #aaa;
						content: "Page " counter(page) " of " counter(pages);
						font-size: 0.8em;
						padding: 0.5em 0;
						vertical-align: top;
						width: 100%;
				}}
			}}
					
			html {{
				font-family: Helvetica;
				font-size: 12px;
				font-weight: normal;
				color: #5D6D7E;
				background-color: transparent;
				margin: 0;
				padding: 0;
				line-height: 150%;
				display: inline;
				width: auto;
				height: auto;
				white-space: normal;
			}}
				
			body {{ 
				margin: 0;
				padding: 0;
			}}
			
			h1 {{
				color: #5D6D7E;
				padding-bottom: 8px;
				border-bottom: 4px solid #5D6D7E;
				margin-bottom: 50px;
			}}
			
			.container {{

			}}
			
			.title {{
				color: rgb(0,145,203);
				font-size: 20px;
				font-weight: bold;
                margin-top: 100px;
				margin-bottom: 10px;
				text-align: center;
			}}

			.subtitle{{
				color: #fff;
				background-color: rgb(0,145,203);
				font-size: 30px;
				font-weight: normal;
				padding-top: 10px;
				padding-bottom: 10px;
				margin-bottom: 50px;
				text-align: center;
			}}

            h1 {{
                color: rgb(0,145,203);
                border-bottom: 4px solid rgb(0,145,203);
            }}

            h2 {{
                color: rgb(0,145,203);
                border-bottom: 2px solid rgb(0,145,203);
            }}

            table {{
            width: 100%;
            max-width: 100%;
            border-spacing: 0;
            border-collapse: collapse;
            font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
            }}

            th {{
                text-align: left;
                border-bottom: 1px solid rgb(0,145,203);
                vertical-align: top;
                padding: 5px;
                color: #5D6D7E;
            }}

            td {{
                vertical-align: top;
                padding: 2px;
                color: #5D6D7E;
            }}


            .attribute {{
                text-align: right;
                color: #5D6D7E;
                font-style: italic;
                width: 100px;
            }}

            .comment {{
                border-left: 10px solid #1B4F72;
                color: #1B4F72;
            }}

            .note {{
                border-left: 10px solid #935116;
                color: #935116;
            }}

            .task {{
                border-left: 10px solid #633974;
                color: #633974;
            }}

            .timestamp {{
                background-color: rgb(0,145,203);
                color: #ffffff;
            }}

            .highlight_note {{
                border-left: 2px solid #935116;
                color: #935116;
            }}

            .highlight_phase {{
                border-left: 2px solid #633974;
                color: #633974;
            }}

            .highlight_task {{
                border-left: 2px solid #633974;
                color: #633974;
            }}

            .highlight_title {{
                font-weight: bold;
            }}
        """

        stylsheet = stylsheet.format(cfg.REPORT_COMPANY, cfg.REPORT_FOOTER)


        buf = '<!DOCTYPE html>'
        buf += '<html>'
        buf += '<head lang="en">'
        buf += '<meta charset="UTF-8">'
        buf += '<title>%s</title>' % cfg.REPORT_TITLE
        buf += '</head>'

        buf += '<body>'
				
        buf += '<div class="container">'
		
        buf += '<div class="title">'
        buf += '<p>%s</p>' % cfg.REPORT_FOOTER
        buf += '</div>'
		
        buf += '<div class="subtitle">'
        buf += '<p>%s</p>' % cfg.REPORT_TITLE
        buf += '<p><strong>** %s **</strong></p>' % container.get('id', "N/A")
        buf += '</div>'
        
        buf += '<p style="page-break-before: always" ></p>'
        buf += "<h1>Overview</h1>\n"
        buf += "Quick Summary.\n"

        buf += "<h2>Incident details</h2>\n"
		
        buf += "<table>\n"
        buf += "<tr><th>ATTRIBUTE</th><th>VALUE</th></tr>\n"
        buf += "<tr><td>TYPE</td><td>%s</td></tr>\n" % container.get('container_type', "N/A")
        buf += "<tr><td>LABEL</td><td>%s</td></tr>\n" % container.get('label', "N/A")
        buf += "<tr><td>ID</td><td>%s</td></tr>\n" % container.get('id', "N/A")
        buf += "<tr><td>NAME</td><td>%s</td></tr>\n" % container.get('name', "N/A")
        buf += "<tr><td>DESCRIPTION</td><td>%s</td></tr>\n" % container.get('description', "N/A")
        buf += "<tr><td>OWNER</td><td>%s</td></tr>\n" % container.get('_pretty_owner', "N/A")
        buf += "<tr><td>CLOSING OWNER</td><td>%s</td></tr>\n" % container.get('_pretty_closing_owner', "N/A")
        buf += "<tr><td>SEVERITY</td><td>%s</td></tr>\n" % container.get('severity', "N/A")
        buf += "<tr><td>SENSITIVITY</td><td>%s</td></tr>\n" % container.get('sensitivity', "N/A")
        buf += "<tr><td>CURRENT PHASE</td><td>%s</td></tr>\n" % container.get('_pretty_current_phase', "N/A")
        buf += "<tr><td>STATUS</td><td>%s</td></tr>\n" % container.get('status', "N/A")
        buf += "<tr><td>FINAL STATUS</td><td>%s</td></tr>\n" % container.get('custom_fields').get('FinalStatus', "N/A")
        buf += "<tr><td>ARTIFACTS</td><td>%s</td></tr>\n" % container.get('artifact_count', "N/A")
        buf += "<tr><td>CREATED</td><td>%s</td></tr>\n" % container.get('create_time', "N/A")
        buf += "<tr><td>CLOSED</td><td>%s</td></tr>\n" % container.get('close_time', "N/A")
        buf += "<tr><td>UPDATED</td><td>%s</td></tr>\n" % container.get('container_update_time', "N/A")
        buf += "</table>\n"
        
        buf += '<p style="page-break-before: always" ></p>'
        buf += "<h1>Details</h1>\n"
        buf += "Quick Summary.\n"

        buf += "<h2>Activity timeline</h2>\n"
		
        """ TESTING SORTING EVERYTHING! """
        activities = []

        for comment in comments.get('data'):
            activities.append([
                comment.get('time'), 
                comment.get('_pretty_user'), 
                'COMMENT', 
                comment.get('comment')])

        for note in notes.get('data'):
            activities.append([
                note.get('create_time'), 
                note.get('_pretty_author'), 
                'NOTE', 
                note.get('title'), 
                note.get('content'), 
                note.get('_pretty_phase')])		
        for phase in phases.get('data'):
            for task in phase.get('tasks'):
                for phasenote in task.get('notes'):
                    activities.append([
                        phasenote.get('create_time'), 
                        phasenote.get('_pretty_author'), 
                        'PHASE', 
                        phase.get('name'),	
                        phasenote.get('_pretty_task'),
                        phasenote.get('title'), 
                        phasenote.get('content')])
                        

        """LOOPING"""
        buf += "<table>\n"

        for activity in sorted(activities):
            activity_timestamp = activity[0][:19].replace("T", " @ ")
            activity_user = activity[1]
            activity_kind = activity[2]

            # comment
            if activity[2] == "COMMENT":
                comment_text = activity[3]
                buf += "<tr><th class=\"timestamp\">&#8618; %s</th><th colspan=\"2\">%s</th><th class=\"comment\">%s</th></tr>\n" % (activity_timestamp, activity_user, activity_kind)
                buf += "<tr><td>&nbsp;</td><td colspan=\"3\">%s</td></tr>\n" % (comment_text)
            # NOTES
            if activity[2] == "NOTE":
                note_title = activity[3]
                note_text = activity[4]
                note_phase = activity[5]
                buf += "<tr><th class=\"timestamp\">&#8618; %s</th><th colspan=\"2\">%s</th><th class=\"note\">%s</th></tr>\n" % (activity_timestamp, activity_user, activity_kind)
                buf += "<tr><td colspan=\"2\">&nbsp;</td><td class=\"attribute\">Phase: </td><td class=\"highlight_note\">&#8677; %s</td></tr>\n" % (note_phase)
                buf += "<tr><td>&nbsp;</td><td colspan=\"3\" class=\"highlight_title\">%s</td></tr>\n" % (note_title)
                buf += "<tr><td>&nbsp;</td><td colspan=\"3\">%s</td></tr>\n" % (note_text)

            # phase
            if activity[2] == "PHASE":
                phase_name = activity[3]
                task_name = activity[4]
                task_title = activity[5]
                task_content = activity[6]
                buf += "<tr><th class=\"timestamp\">&#8618; %s</th><th colspan=\"2\">%s</th><th class=\"task\">%s</th></tr>\n" % (activity_timestamp, activity_user, activity_kind)
                buf += "<tr><td colspan=\"2\">&nbsp;</td><td class=\"attribute\">Phase: </td><td class=\"highlight_phase\">&#8677; %s</td></tr>\n" % (phase_name)
                buf += "<tr><td colspan=\"2\">&nbsp;</td><td class=\"attribute\">Task: </td><td class=\"highlight_task\">&#8674; %s</td></tr>\n" % (task_name)
                buf += "<tr><td>&nbsp;</td><td colspan=\"3\" class=\"highlight_title\">%s</td></tr>\n" % (task_title)
                buf += "<tr><td>&nbsp;</td><td colspan=\"3\">%s</td></tr>\n" % (task_content)
            
            buf += "<tr><td colspan=\"4\">&nbsp;</td></tr>\n" #empty
        
        
        buf += "</table>\n"

		
        buf += '</div>'
		
        buf += '</body>'
        buf += '</html>'
		
		
        # GENERATE PDF
        HTML(string=buf).write_pdf(filename, stylesheets=[CSS(string=stylsheet)])
		
    except Exception as e:
        print("Error %s:" % e)



""" get_details() """
def get_details(server, token, container, kind):
    try:
        """Configuring Phantom URL"""

        logging.debug('Configuring Phantom URL')
        if(kind == "container"):
            url = "https://%s/rest/container/%s/?include_expensive&pretty" % (server, container)
        elif(kind == "comments"):
            url = "https://%s/rest/container/%s/comments/?include_expensive&pretty&order=time&order=desc" % (server, container)
        elif(kind == "artifacts"):
            url = "https://%s/rest/container/%s/artifacts/?include_expensive&pretty" % (server, container)
        elif(kind == "actions"):
            url = "https://%s/rest/container/%s/actions/?include_expensive&pretty" % (server, container)
        elif(kind == "attachements"):
            url = "https://%s/rest/container/%s/attachements/?include_expensive&pretty" % (server, container)
        elif(kind == "audit"):
            url = "https://%s/rest/container/%s/audit/?include_expensive&pretty" % (server, container)
        elif(kind == "phases"):
            url = "https://%s/rest/container/%s/phases/?include_expensive&pretty" % (server, container)
        elif(kind == "notes"):
            url = "https://%s/rest/container/%s/notes/?include_expensive&pretty" % (server, container)
        else:
            logging.critical('Error: %s unknown kind', kind)
            exit()

        headers = {
            "ph-auth-token": token
        }
        
        """Running query"""

        logging.info('Collecting data for %s' % kind) 
        
        r = requests.get(url, headers=headers, verify=True)

        """Verifying if query was successful"""
        if (r is None or (r.status_code != 200 and r.status_code != 400)):
            if r is None:
                logging.critical('Error running query')
            else:
                logging.critical('Error: %s - %s', r.status_code, json.loads(r.text)['message'])
                empty_json = '{}'
            return json.loads(empty_json)

        """Query was successful"""
        return json.loads(r.text)
        
    except Exception as e:
        logging.critical('Error: %s', e.args[0])


""" __main__ """
if __name__ == "__main__":
    """Runs main routine."""
    logging.debug('Calling "main" function')
    main()
    logging.debug('Finished!')
