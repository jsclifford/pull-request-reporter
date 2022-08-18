import os
from pprint import pprint
from github import Github
import datetime


def init_github():
    gh = Github(os.environ.get('GITHUB_ACCESS_TOKEN'))
    return gh


def get_pull_request(gh, repository: str, previous_date: datetime):
    # Get Repos
    repo = gh.get_repo(repository)
    pulls = repo.get_pulls(state='all', sort='updated', direction='desc')
    pr_details = []
    pr_summary = {
        "open": 0,
        "closed": 0,
        "draft": 0
    }
    for pr in pulls:
        if pr.updated_at > previous_date:
            pr_table_row = f"<tr><td><a href=\"{pr.html_url}\">{pr.number}</a></td><td>{pr.state}</td><td>{pr.created_at.date()}<td>{pr.updated_at.date()}</td><td>{pr.title}</td></tr>"
            pr_details.append(pr_table_row)

            if pr.state == 'open':
                pr_summary['open'] = pr_summary['open'] + 1
            elif pr.state == 'closed':
                pr_summary['closed'] = pr_summary['closed'] + 1
            elif pr.draft:
                pr_summary['draft'] = pr_summary['draft'] + 1
            else:
                print(
                    f"No state was matched. Status: {pr.state} ; Draft: {pr.draft}")
        else:
            print(
                f"Found {len(pr_details)} PRs updated after {previous_date.date()}")
            break

    return {'details': pr_details, 'summary': pr_summary}


def html_body(repository, previous_date: datetime, details: list, summary: dict):
    table_rows = ""
    for row in details:
        table_rows = f"{table_rows} {row}"

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
<style>
table, th, td {{
  border: 1px solid black;
  border-collapse: collapse;
}}
</style>
</head>
<body>
  <h2>Overview:</h2>
  <ul>
    <li>PRs Updated After {previous_date.date()}</li>
    <li>Repository: <a href="https://github.com/{repository}">{repository}</a></li>
    <li>Open: {summary['open']}</li>
    <li>Closed: {summary['closed']}</li>
    <li>Draft: {summary['draft']}</li>
  </ul>
  <br />
  <hr />
  <br />
  <h2>PR Details:</h2>
  <table style="width: 100%">
    <tr>
      <th><strong>ID</strong></th>
      <th><strong>Status</strong></th>
      <th><strong>Created Date</strong></th>
      <th><strong>Updated Date</strong></th>
      <th><strong>Title</strong></th>
    </tr>
    {table_rows}
  </table>
</body>
</html>
"""

    return html_content


def html_body_template(repository, previous_date: datetime, details: list, summary: dict):
    table_rows = ""
    for row in details:
        table_rows = f"{table_rows} {row}"

    html_content = f"""
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
    <meta charset="utf-8"> <!-- utf-8 works for most cases -->
    <meta name="viewport" content="width=device-width"> <!-- Forcing initial-scale shouldn't be necessary -->
    <meta http-equiv="X-UA-Compatible" content="IE=edge"> <!-- Use the latest (edge) version of IE rendering engine -->
    <meta name="x-apple-disable-message-reformatting">  <!-- Disable auto-scale in iOS 10 Mail entirely -->
    <title></title> <!-- The title tag shows in email notifications, like Android 4.4. -->

    <link href="https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700" rel="stylesheet">

    <!-- CSS Reset : BEGIN -->
    <style>
    html,
    body {{
        margin: 0 auto !important;
        padding: 0 !important;
        height: 100% !important;
        width: 100% !important;
        background: #f1f1f1;
    }}

    /* What it does: Stops email clients resizing small text. */
    * {{
        -ms-text-size-adjust: 100%;
        -webkit-text-size-adjust: 100%;
    }}

    /* What it does: Centers email on Android 4.4 */
    div[style*="margin: 16px 0"] {{
        margin: 0 !important;
    }}

    /* What it does: Stops Outlook from adding extra spacing to tables. */
    table,
    td {{
        mso-table-lspace: 0pt !important;
        mso-table-rspace: 0pt !important;
    }}

    /* What it does: Fixes webkit padding issue. */
    table {{
        border-spacing: 0 !important;
        border-collapse: collapse !important;
        table-layout: fixed !important;
        margin: 0 auto !important;
    }}

    table.prdetails, .prdetails th, .prdetails td {{
      border: 1px solid black;
      border-collapse: collapse;
    }}

    /* What it does: Uses a better rendering method when resizing images in IE. */
    img {{
        -ms-interpolation-mode:bicubic;
    }}

    /* What it does: Prevents Windows 10 Mail from underlining links despite inline CSS. Styles for underlined links should be inline. */
    a {{
        text-decoration: none;
    }}

    /* What it does: A work-around for email clients meddling in triggered links. */
    *[x-apple-data-detectors],  /* iOS */
    .unstyle-auto-detected-links *,
    .aBn {{
        border-bottom: 0 !important;
        cursor: default !important;
        color: inherit !important;
        text-decoration: none !important;
        font-size: inherit !important;
        font-family: inherit !important;
        font-weight: inherit !important;
        line-height: inherit !important;
    }}

    /* What it does: Prevents Gmail from displaying a download button on large, non-linked images. */
    .a6S {{
        display: none !important;
        opacity: 0.01 !important;
    }}

    /* What it does: Prevents Gmail from changing the text color in conversation threads. */
    .im {{
        color: inherit !important;
    }}

    /* If the above doesn't work, add a .g-img class to any image in question. */
    img.g-img + div {{
        display: none !important;
    }}

    /* What it does: Removes right gutter in Gmail iOS app: https://github.com/TedGoas/Cerberus/issues/89  */
    /* Create one of these media queries for each additional viewport size you'd like to fix */

    /* iPhone 4, 4S, 5, 5S, 5C, and 5SE */
    @media only screen and (min-device-width: 320px) and (max-device-width: 374px) {{
        u ~ div .email-container {{
            min-width: 320px !important;
        }}
    }}
    /* iPhone 6, 6S, 7, 8, and X */
    @media only screen and (min-device-width: 375px) and (max-device-width: 413px) {{
        u ~ div .email-container {{
            min-width: 375px !important;
        }}
    }}
    /* iPhone 6+, 7+, and 8+ */
    @media only screen and (min-device-width: 414px) {{
        u ~ div .email-container {{
            min-width: 414px !important;
        }}
    }}

    </style>

    <!-- CSS Reset : END -->

    <!-- Progressive Enhancements : BEGIN -->
    <style>

      .primary{{
      background: #0d0cb5;
    }}
    .bg_white{{
      background: #ffffff;
    }}
    .bg_light{{
      background: #fafafa;
    }}
    .bg_black{{
      background: #000000;
    }}
    .bg_dark{{
      background: rgba(0,0,0,.8);
    }}
    .email-section{{
      padding:2.5em;
    }}

    /*BUTTON*/
    .btn{{
      padding: 5px 15px;
      display: inline-block;
    }}
    .btn.btn-primary{{
      border-radius: 5px;
      background: #0d0cb5;
      color: #ffffff;
    }}
    .btn.btn-white{{
      border-radius: 5px;
      background: #ffffff;
      color: #000000;
    }}
    .btn.btn-white-outline{{
      border-radius: 5px;
      background: transparent;
      border: 1px solid #fff;
      color: #fff;
    }}

    h1,h2,h3,h4,h5,h6{{
      font-family: 'Poppins', sans-serif;
      color: #000000;
      margin-top: 0;
    }}

    body{{
      font-family: 'Poppins', sans-serif;
      font-weight: 400;
      font-size: 15px;
      line-height: 1.8;
      color: rgba(0,0,0,.4);
    }}

    a{{
      color: #0d0cb5;
    }}

    table{{
    }}
    /*LOGO*/

    .logo h1{{
      margin: 0;
    }}
    .logo h1 a{{
      color: #000000;
      font-size: 20px;
      font-weight: 700;
      text-transform: uppercase;
      font-family: 'Poppins', sans-serif;
    }}

    .navigation{{
      padding: 0;
    }}
    .navigation li{{
      list-style: none;
      display: inline-block;;
      margin-left: 5px;
      font-size: 13px;
      font-weight: 500;
    }}
    .navigation li a{{
      color: rgba(0,0,0,.4);
    }}

    /*HERO*/
    .hero{{
      position: relative;
      z-index: 0;
    }}
    .hero .overlay{{
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      content: '';
      width: 100%;
      background: #000000;
      z-index: -1;
      opacity: .3;
    }}
    .hero .icon{{
    }}
    .hero .icon a{{
      display: block;
      width: 60px;
      margin: 0 auto;
    }}
    .hero .text{{
      color: rgba(255,255,255,.8);
    }}
    .hero .text h2{{
      color: #ffffff;
      font-size: 30px;
      margin-bottom: 0;
    }}


    /*HEADING SECTION*/
    .heading-section{{
    }}
    .heading-section h2{{
      color: #000000;
      font-size: 20px;
      margin-top: 0;
      line-height: 1.4;
      font-weight: 700;
      text-transform: uppercase;
    }}
    .heading-section .subheading{{
      margin-bottom: 20px !important;
      display: inline-block;
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 2px;
      color: rgba(0,0,0,.4);
      position: relative;
    }}
    .heading-section .subheading::after{{
      position: absolute;
      left: 0;
      right: 0;
      bottom: -10px;
      content: '';
      width: 100%;
      height: 2px;
      background: #0d0cb5;
      margin: 0 auto;
    }}

    .heading-section-white{{
      color: rgba(255,255,255,.8);
    }}
    .heading-section-white h2{{
      font-family: 
      line-height: 1;
      padding-bottom: 0;
    }}
    .heading-section-white h2{{
      color: #ffffff;
    }}
    .heading-section-white .subheading{{
      margin-bottom: 0;
      display: inline-block;
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 2px;
      color: rgba(255,255,255,.4);
    }}


    .icon{{
      text-align: center;
    }}
    .icon img{{
    }}


    /*SERVICES*/
    .services{{
      background: rgba(0,0,0,.03);
    }}
    .text-services{{
      padding: 10px 10px 0; 
      text-align: center;
    }}
    .text-services h3{{
      font-size: 16px;
      font-weight: 600;
    }}

    .services-list{{
      padding: 0;
      margin: 0 0 20px 0;
      width: 100%;
      float: left;
    }}

    .services-list img{{
      float: left;
    }}
    .services-list .text{{
      width: calc(100% - 60px);
      float: right;
    }}
    .services-list h3{{
      margin-top: 0;
      margin-bottom: 0;
    }}
    .services-list p{{
      margin: 0;
    }}

    /*BLOG*/
    .text-services .meta{{
      text-transform: uppercase;
      font-size: 14px;
    }}

    /*TESTIMONY*/
    .text-testimony .name{{
      margin: 0;
    }}
    .text-testimony .position{{
      color: rgba(0,0,0,.3);

    }}


    /*VIDEO*/
    .img{{
      width: 100%;
      height: auto;
      position: relative;
    }}
    .img .icon{{
      position: absolute;
      top: 50%;
      left: 0;
      right: 0;
      bottom: 0;
      margin-top: -25px;
    }}
    .img .icon a{{
      display: block;
      width: 60px;
      position: absolute;
      top: 0;
      left: 50%;
      margin-left: -25px;
    }}



    /*COUNTER*/
    .counter{{
      width: 100%;
      position: relative;
      z-index: 0;
    }}
    .counter .overlay{{
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      content: '';
      width: 100%;
      background: #000000;
      z-index: -1;
      opacity: .3;
    }}
    .counter-text{{
      text-align: center;
    }}
    .counter-text .num{{
      display: block;
      color: #ffffff;
      font-size: 34px;
      font-weight: 700;
    }}
    .counter-text .name{{
      display: block;
      color: rgba(255,255,255,.9);
      font-size: 13px;
    }}


    /*FOOTER*/

    .footer{{
      color: rgba(255,255,255,.5);

    }}
    .footer .heading{{
      color: #ffffff;
      font-size: 20px;
    }}
    .footer ul{{
      margin: 0;
      padding: 0;
    }}
    .footer ul li{{
      list-style: none;
      margin-bottom: 10px;
    }}
    .footer ul li a{{
      color: rgba(255,255,255,1);
    }}


    @media screen and (max-width: 500px) {{

      .icon{{
        text-align: left;
      }}

      .text-services{{
        padding-left: 0;
        padding-right: 20px;
        text-align: left;
      }}

    }}
    </style>


</head>

<body width="100%" style="margin: 0; padding: 0 !important; mso-line-height-rule: exactly; background-color: #222222;">
	<center style="width: 100%; background-color: #f1f1f1;">
    <div style="display: none; font-size: 1px;max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; mso-hide: all; font-family: sans-serif;">
      &zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;
    </div>
    <div style="max-width: 600px; margin: 0 auto;" class="email-container">
    	<!-- BEGIN BODY -->
      <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: auto;">
      	<tr>
          <td valign="top" class="bg_white" style="padding: 1em 2.5em;">
          	<table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
          		<tr>
          			<td width="80%" class="logo" style="text-align: left;">
			            <h1><a href="#">Github Pull Request Report</a></h1>
			          </td>
          		</tr>
          	</table>
          </td>
	      </tr><!-- end tr -->
				<tr>
          <td valign="middle" class="hero bg_white" style="background-image: url(https://github.com/ColorlibHQ/email-templates/raw/master/2/images/bg_1.jpg); background-size: cover; height: 400px;">
          	<div class="overlay"></div>
            <table>
            	<tr>
            		<td>
            			<div class="text" style="padding: 0 3em; text-align: center;">
            				<h2>Repo: <a href="https://github.com/{repository}">{repository}</a></h2>
            				<div class="icon">
	            				<a href="https://github.com/{repository}">
	                      <img src="https://github.com/ColorlibHQ/email-templates/raw/master/2/images/002-play-button.png" alt="" style="width: 60px; max-width: 600px; height: auto; margin: auto; display: block;">
	                    </a>
	                  </div>
            			</div>
            		</td>
            	</tr>
            </table>
          </td>
	      </tr><!-- end tr -->
	      <tr>
		      <td class="bg_white">
		        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
		          <tr>
		            <td class="bg_white email-section">
		            	<div class="heading-section" style="text-align: center; padding: 0 30px;">
		              	<h2>Overview</h2>
		              	<p>Pull Requests Created or Updated After {previous_date.date()}.</p>
		            	</div>
		            	<table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
		            		<tr>
		            			<td valign="top" width="33.333%" style="padding-top: 20px;" class="services">
                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                          <tr>
                            <td class="icon">
                              <img src="https://github.com/ColorlibHQ/email-templates/raw/master/2/images/001-diet.png" alt="" style="width: 60px; max-width: 600px; height: auto; margin: auto; display: block;">
                            </td>
                          </tr>
                          <tr>
                            <td class="text-services">
                            	<h3>Open</h3>
                             	<p>{summary['open']}</p>
                            </td>
                          </tr>
                        </table>
                      </td>
                      <td valign="top" width="33.333%" style="padding-top: 20px; background: rgba(0,0,0,.08);" class="services">
                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                          <tr>
                            <td class="icon">
                              <img src="https://github.com/ColorlibHQ/email-templates/raw/master/2/images/001-diet.png" alt="" style="width: 60px; max-width: 600px; height: auto; margin: auto; display: block;">
                            </td>
                          </tr>
                          <tr>
                            <td class="text-services">
                            	<h3>Closed</h3>
                             	<p>{summary['closed']}</p>
                            </td>
                          </tr>
                        </table>
                      </td>
                      <td valign="top" width="33.333%" style="padding-top: 20px;" class="services">
                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                          <tr>
                            <td class="icon">
                              <img src="https://github.com/ColorlibHQ/email-templates/raw/master/2/images/003-recipe-book.png" alt="" style="width: 60px; max-width: 600px; height: auto; margin: auto; display: block;">
                            </td>
                          </tr>
                          <tr>
                            <td class="text-services">
                            	<h3>Draft</h3>
                              <p>{summary['draft']}</p>
                            </td>
                          </tr>
                        </table>
                      </td>
                    </tr>
		            	</table>
		            </td>
		          </tr><!-- end: tr -->
		          <tr>
		            <td class="bg_light email-section" style="width: 100%;">
		            	<table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
		            		<tr>
		            			<td valign="middle" width="50%">
                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                          <tr>
                            <td>
                              <img src="https://github.com/ColorlibHQ/email-templates/raw/master/2/images/about.jpg" alt="" style="width: 100%; max-width: 600px; height: auto; margin: auto; display: block;">
                            </td>
                          </tr>
                        </table>
                      </td>
                      <td valign="middle" width="50%">
                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                          <tr>
                            <td class="text-services" style="text-align: left; padding-left:25px;">
                            	<div class="heading-section">
								              	<h2>Pull Request Details</h2>
								              	<p>This includes open, closed, and draft pull requests</p>
								              	<p><a href="https://github.com/{repository}/pulls" class="btn btn-primary">View all Pull Requests</a></p>
								            	</div>
                            </td>
                          </tr>
                        </table>
                      </td>
                    </tr>
		            	</table>
		            </td>
		          </tr><!-- end: tr -->
              <tr>
                <td>
                  <table class="prdetails" style="width: 100%">
                    <tr>
                      <th>ID</th>
                      <th>Status</th>
                      <th>Created Date</th>
                      <th>Updated Date</th>
                      <th>Title</th>
                    </tr>
                    {table_rows}
                  </table>
                </td>
              </tr>
            </table>
          </td>
        </tr><!-- end: tr -->
        <tr>
        	<td valign="middle" class="bg_black footer email-section">
        		<table>
            	<tr>
                <td valign="top" width="33.333%">
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                    <tr>
                      <td style="text-align: left; padding-right: 10px;">
                      	<p>&copy; 2018 Corporate. All Rights Reserved</p>
                      </td>
                    </tr>
                  </table>
                </td>
                <td valign="top" width="33.333%">
                  <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                    <tr>
                      <td style="text-align: right; padding-left: 5px; padding-right: 5px;">
                      	<p><a href="#" style="color: rgba(255,255,255,.4);">Unsubcribe</a></p>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
        	</td>
        </tr>
      </table>

    </div>
  </center>
</body>
</html> 
"""
    return html_content
