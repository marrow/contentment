# encoding: utf-8

from template import root, theme, header, menu, footer, default

from datetime import datetime

from web.extras.contentment.components.asset.model import db
from web.extras.contentment.components.asset.model import *
from web.extras.contentment.components.folder.model import Folder
from web.extras.contentment.components.alias.model import Alias
from web.extras.contentment.components.page.model import Page
from web.extras.contentment.components.event.model import Event, EventContact
from web.extras.contentment.components.search.model import Search
from web.extras.contentment.themes.architecture.model import ArchitectureTheme


# Delete the default theme and update to use our custom theme.
theme.delete()
theme = ArchitectureTheme(name="theme", title="Architecture Theme", immutable=True); theme.save() ; theme.attach(root)
root.properties['org-contentment-theme'] = 'web.extras.contentment.themes.architecture'
root.properties['org-contentment-option-attribution'] = False
root.save()

# Update the header to be -our- header.
header.content = u"""h1. "Town of Comox":/\n\nVillage by the sea.""" ; header.save()

# Update the menu to be -our- menu, etc.
menu.content = u"""<ul>
    <li class="important"><a href="/">Home</a></li
    ><li><a href="/by-election/">Municipal By Election</a></li
    ><li><a href="/discover/">Discover Comox</a><ul>
            <li><a href="/discover/overview">Comox Overview</a></li
            ><li><a href="/discover/mayor">Mayor's Message</a></li
            ><li><a href="/discover/gethere">How to Get Here</a></li
            ><li><a href="/discover/parks">Parks &amp; Playing Fields</a></li
            ><li><a href="/discover/filberg">Filberg Park</a></li
            ><li><a href="/discover/rec-tour">Recreation & Tourism</a></li
            ><li><a href="/discover/links">Community Links</a></li
            ><li><a href="/discover/album">Comox Album</a></li
            ><li><a href="/discover/deer">Expect Deer</a></li
            ><li><a href="/discover/events">Community Events</a></li
            ><li><a href="/discover/hmcscomox">HMCS Comox</a></li>
        </ul></li
    ><li><a href="/hall/">Town Hall</a><ul>
        <li><a href="/hall/announcements">Announcements</a></li
        ><li><a href="/hall/bylaws">Bylaws</a></li
        ><li><a href="/hall/departments">Departments</a></li
        ><li><a href="/hall/meetings">Meetings</a><ul>
            <li><a href="/hall/meetings/agendas">Agendas</a></li
            ><li><a href="/hall/meetings/minutes">Minutes</a></li
            ><li><a href="/hall/meetings/cm-dates">2010 Council Meeting Dates</a></li>
        </ul></li
       ><li><a href="/hall/council">Mayor and Council</a></li
    ></ul></li
    ><li><a href="/services/">Services</a><ul>
        <li><a href="/services/bus-licence">Business Licensing</a></li
        ><li><a href="/services/recycling">Recycling and Garbage-2010</a></li
        ><li><a href="/services/marina">Comox Bay Marina</a></li
        ><li><a href="/services/maps">Maps</a></li
        ><li><a href="/services/marinas">Marinas</a></li
        ><li><a href="/services/parks">Parks</a></li
        ><li><a href="/services/sewer">Sewer</a></li
        ><li><a href="/services/recreation>Comox Recreation Centre</a></li
        ><li><a href="/services/finance">Finance Department</a></li>
    </ul></li
    ><li><a href="/interactive/">Interactive</a><ul>
        <li><a href="/interactive/feedback">Feedback</a></li
        ><li><a href="/interactive/blog">Comox Herald (blog)</a></li
        ><li><a href="/interactive/questions">Questions and Answers</a></li
        ><li><a href="/interactive/tax-search">Tax Search</a></li
        ><li><a href="/interactive/homegrant">Home Owner Grant</a></li
        ><li><a href="/interactive/forms">Application Forms</a></li>
    </ul></li
    ><li><a href="/financial-plan">2010 Financial Plan</a></li
    ><li><a href="/water">Water</a></li>
</ul>"""
menu.save()


footer.content = u"""<div id="copyright">
    Copyright © 2010 Town of Comox. All Rights Reserved.
</div>
<div style="padding-left: 60px;">
<table id="footer-links" >
<tr valign=top>
    <td width="150">
        <h3>Town Hall</h3>
        <ul><li><a title="Mayor and Council" href="town-hall/mayor-and-council" target="_self">Mayor & Council</a></li><li><a title="Town Contacts" href="/hall/departments" target="_self">Departments</a></li><li><a href="/hall/meetings" target="_self">Meetings</a></li><li><a title="Forms" href="interactive/forms" target="_self">Application Forms</a></li><li><a title="Announcements" href="/hall/announcements" target="_self">Announcements</a></li><li><a title="BYLAWS" href="/hall/bylaws" target="_self">Bylaws</a></li><li><a title="Q and A" href="interactive/questions-and-answers" target="_self">Questions</a></li><li><a title="Employment" href="hall/departments/corporate-admin-pages/employment-opportunities" target="_self">Employment</a></li></ul>
    </td>
    <td width="150">
        <h3>Living Here</h3>
        <ul><strong>Recreation</strong><li><a title="parks" href="/discover/parks" target="_self">Parks & Fields</a></li><li><a title="recycling" href="services/garbage-and-recycling" target="_self">Garbage/Recycling</a></li><li><a title="Services" href="services" target="_self">Other Services</a></li><li><a title="Community Events" href="/discover/events" target="_self">Events</a></li><li><a href="town-hall/departments/corporate-admin-pages/comox-news/" target="_self">Newsletter</a></li></ul>
    </td>
    <td width="150">
        <h3>Visiting</h3>
        <ul><li><a title="How to Get Here" href="discover-comox/how-to-get-here" target="_self">Getting Here</a></li><li><a title="Comox Overview" href="/discover/overview" target="_self">Comox Overview</a></li><li><a title="Recreation & Tourism" href="discover/rec-tour" target="_self">Things to do</a></li><li><a title="Recreation & Tourism" href="discover/rec-tour" target="_self">Places to See</a></li><li><a title="maps" href="town-hall/maps" target="_self">Maps</a></li><li><a title="Marinas" href="discover-comox/marinas" target="_self">Marina</a></li></ul>
    </td>
    <td>
        <h3>Contact Information</h3>
        <ul><li><a title="e-mail" href="contact-info" target="_self">General Email</a></li><li><a title="Mayor and Council" href="town-hall/mayor-and-council" target="_self">Mayor and Council</a></li><li><a title="Town Contacts" href="town-hall/town-contacts" target="_self">Department Heads</a></li><li><a title="Feedback" href="interactive/feedback" target="_self">Leave Comment</a></li><li>Comox Town Hall <br />1809 Beaufort Ave;<br />Comox, BC V9M 1R9 <br/>(Monday - Friday 8:30am to 4:30pm <br/> closed on Stat Holidays)</li><li>Ph:250-339-2202</li><li>Fx:250-339-7110</li></ul>
    </td>
</tr>
</table>
</div>"""
footer.save()


default.content = u"""h1. Welcome to the Town of Comox\n\nThe material provided here is designed to help you become better acquainted with the Town of Comox and all it has to offer both visitors and residents. It is designed to assist you in obtaining the information you need to live, work, conduct business, and have fun in our community."""
default.save()



discover = Folder(name="discover", title=u"Discover Comox", description=u"", default="default") ; discover.save() ; discover.attach(root)


# _ = Page(name="", title=u"", description=u"", content=u"""h1. Welcome to the Town of Comox""") ; _.save() ; _.attach(discover)
_ = Page(name="default", title=u"Discover Comox", description=u"", content=u"""h1. Welcome to the Town of Comox

Welcome to the Town of Comox Electronic Information System. The material provided here is designed to help you become better acquainted with the Town of Comox and all it has to offer both visitors and residents. It is designed to assist you in obtaining the information you need to live, work, conduct business, and have fun in our community.

We hope you will find our web site helpful. We will be updating it regularly, and with your help, in the form of feedback, expanding it in the future. If you would like further information about the Town or this home page, please call the Town of Comox at (250) 339-2202 or send us an email by selecting the feedback option on the navigation bar.

The Town of Comox is situated on the east coast of Vancouver Island, approximately 115Km north of Nanaimo. Together with the City of Courtenay and the Village of Cumberland, Comox lies in an area known as The Comox Valley situated between the Beaufort Range and Comox Glacier in the west, and the Strait of Georgia in the East.

Mission Statement: Council will endeavor to manage growth in a way that maintains and enhances community livability. It will ensure that the character of its residential areas are protected and that its commercial areas are attractive, viable and complementary to their neighbourhood. It will protect important natural areas, provide green spaces, recreational opportunities and facilities to meet the needs of its citizens. It will retain an ambiance as a village by the sea.

"Overview...":/discover/overview""") ; _.save() ; _.attach(discover)


_ = Page(name="overview", title=u"Comox Overview", description=u"", content=u"""h1. Comox Overview

h2. History

First settled by the Salish, the name Comox is derived from the Indian word "Koumuckthay", meaning "Land of Plenty". The "Port of Comox":http://www.comoxfishermanswharf.com/marine_history/ was founded in the mid 1800's on the slopes of the Comox Peninsula. Overlooking the protected waters of Comox Harbour, it was an important port for the ships of the Royal Navy and transport steamers.

Today Comox is primarily residential in nature, with a population of about 12,000 and covers some 1500 hectares. Located in the centre of a rich agricultural area producing potatoes, vegetables, fruit and dairy products, Comox retains a friendly village atmosphere.

Our moderate climate, unsurpassed recreational opportunities and comprehensive community services are just three of the reasons that Comox is rapidly becoming known as a retirement mecca.

h2. Tourism

"*Comox Valley Visitor Centre*":http://www.comoxvalleychamber.com/visitor-centre

"Tourism":recreation-tourism is a growth industry with Comox being ideally situated to act as a base for the enjoyment of the wonderful outdoor resources available in the area.

p(fr). !http://comox.ca/site-graphics/glacier1page.jpg!

Comox is well served by a modern new highway south to Nanaimo and Victoria, and north to Campbell River. The older Island Highway serves the logging, mining and fishing communities north of Campbell River. There is a "ferry":http://www.bcferries.bc.ca/ to Powell River on the Canadian Mainland, and&nbsp;"Comox Valley Airport":http://www.comoxairport.com/ which has several&nbsp;scheduled flights daily to the City of Vancouver and island destinations. BC Transit operates a "local bus service":http://www.busonline.ca/regions/com/?p=2.list within the Comox Valley.

h2. CFB Comox

"CFB Comox":http://www.airforce.forces.ca/19w-19e/index-eng.asp is a integral part of the community. Having been founded in 1942 as a Royal Air Force base, CFB Comox has played a major role in shaping and supporting the community. The primary responsibilities of CFB Comox are Search and Rescue operations, maritime patrols and support of naval and air force defences. In addition to the essential roles the base plays for the community, BC and Canada, CFB Comox is a large supporter of community events routinely supplying volunteers and equipment wherever needed.

h2. Amenities

Amenities located within the town include a number of "marinas":marinas for commercial, sports fishing boats, and pleasure craft including a large number of sailboats. You will also find a well equipped volunteer fire department and commercial airport in Comox. A 9 hole golf course, modern community centre, library, the largest hospital north of Nanaimo which included extended care and psychiatric wings, and 125 hectares of parks, playing fields and reserves also service the needs of the community.

Education is provided in four Elementary and one High School which are in the "School District 71 area.":http://sd71.bc.ca/ "North Island College":http://www.nic.bc.ca/, which provides equivalency, Diploma and university transfer courses together with a wealth of leisure programs is also located in the Comox Valley.

h2. Leisure

The renowned sailing of the Inside Passage, wind surfing in the protected waters behind Goose Spit, world class cross country and downhill skiing on "Mount Washington":http://www.mountwashington.ca/ , hiking in the mountains and lakes of Strathcona Provincial Park are all accessible from the Comox Valley. For the fisherman we can offer river, lake and salt water angling, for the golfer we have half a dozen courses and for the kids a day at the beach. For the family there is camping, canoeing, kayaking, mountain biking and horse riding.

If you just want to relax; then pull up a bench in one of our many "parks":parks-fields and admire the view. Perhaps try your hand at bird spotting in one of the nearby sanctuaries, or amble down to one of our marinas, and sit and watch the comings and goings of sail and motor craft, ending the day with some fresh Halibut, Salmon, Tuna, Crab or Prawns bought directly from a fishing boat at the wharf.

A visit to one of our four museums can be very rewarding. "The Comox Archives and Museum Society":http://www.comoxmuseum.ca/ is located in downtown Comox. Every month there is a new display of interest to Comox Residents. Learn about mining in "Cumberland":http://www.cumberlandmuseum.ca/cgi-bin/show_home.cgi, dinosaurs in "Courtenay":http://www.courtenaymuseum.ca/ or aviation at "CFB Comox.":http://www.comoxairforcemuseum.ca/

If you are a photographer or artist how about a foreground of tall masts screening a blue expanse of water, perhaps broken by a diminutive tug pulling a log-boom. And in the near distance (the other side of the bay) a mountain skyline dominated by the white splash of the Comox Glacier all set against a blue sky. If you prefer something a little more intimate, you may like to set up your easel or unsheathe your long lens in the gazebo set in the wetland sanctuary at the head of the harbour and try for a goose, swan, duck, crane, or one of the many other birds and fowls frequenting the area. Eagle and Harbour Seal call Comox their home, and deer still wander our streets looking for an unprotected vegetable garden or fruit tree.

h2. Entertainment

Comox, and the surrounding area boasts a variety of world class artists. Each year on the first weekend in August the "Filberg Festival":http://www.filbergfestival.com/ is held in Comox. This feast for the senses provides a forum for hundreds of artists and performers to display their work and entertain for three days. "CYMC":http://www.cymc.ca/, a three week summer music festival and workshop attracts each year young musicians from far afield.

bq. "Yes, Comox has it all, culture, sports, education, scenic beauty the "great outdoors", mild climate and the village lifestyle. All here for us to experience, maintain and enjoy."
""") ; _.save() ; _.attach(discover)


_ = Page(name="mayor", title=u"Mayor's Message", description=u"", content=u"""h1. Mayor's Message

Comox is a wonderful community, located half way up Vancouver Island, at the northern end of the Strait of Georgia. We are a jumping off place for vessels transiting to Alaska or heading to Desolation Sound. We are a friendly community that is concerned about our environment and cherishes our green spaces.</p>

The Town is in excellent financial shape while our taxes are one of the lowest on Vancouver Island. Our airport, which services the entire Comox Valley, has regularly scheduled flights to both Vancouver (30 minutes away) and Calgary (1 hour 15 minutes away). This may be one of the reasons that so many people choose our valley to vacation. It may also be that we have the third largest ski resort in British Columbia, our own glacier, fabulous mountains and mountain biking, kayaking, hiking, fishing and year round golf. Or it could just be that we have wonderful people who care about visitors. We would like you to visit and enjoy our wonderful shops, restaurants, pubs, parks, playgrounds, golf courses and marina.

Comox is open for business, we'd love to see you here.

Paul Ives, Mayor""") ; _.save() ; _.attach(discover)


_ = Page(name="directions", title=u"How to Get Here", description=u"", content=u"""h1. Getting to the Comox Valley

Comox is located on the eastern side of Vancouver Island, 107 km (66 miles) north of Nanaimo and 220 km (137 miles) north of Victoria. The four lane Inland Island Highway #19 makes travel to Comox faster than before. The trip between Nanaimo and Comox now takes less than an hour and a half. The older ocean side highway, Highway 19A, provides an alternate route in which visitors can enjoy the scenery of Vancouver Island's coastal communities. This can be driven in a couple of hours, but may take you days if you take advantage of the many campsites, motels and resorts.

* "Province of British Columbia; Ministry of Transportation":http://www.gov.bc.ca/bvprd/bc/channel.do?action=ministry&channelID=-8394&navId=NAV_ID_-8394
* "Comox Valley Visitor Centre":http://www.comoxvalleychamber.com/visitor-centre

h2. By Ferry...

p(fr). !http://comox.ca/site-graphics/ferries.png!

There is frequent ferry service from the mainland to Victoria or Nanaimo. An alternate route is to head north from Vancouver on highway #101 and take the Powell River ferry to Comox.

|_. Website | "BC Ferries":http://www.bcferries.bc.ca/ |
|_. Toll | 1 250 386-3431 |
|_. Toll-Free | 1 888 223-3779 (in British Columbia) |

h2. By Bus...

p(fr). !http://comox.ca/site-graphics/greyline.png!

Daily bus service offers quick and affordable transport from Vancouver and throughout the Island. Locally there is bus service in the 3 municipalities of Courtenay, Comox and Cumberland. 
HandyDart buses are available for people with disabilities.

h3. Island Coach Lines (Laidlaw)

|_. Toll | 1 250 385-4411 |
|_. Toll-Free | 1 800 318-0818 |

"Comox Valley Transit System":http://www.bctransit.com/regions/com/

|_. Local: | 1 250 339-5453 |

h2. By Air...

"The Comox Valley Airport(YQQ)":http://www.comoxairport.com/ is served by a variety of airlines:

"Pacific Coastal Airlines":http://www.pacific-coastal.com/ provides air service from Comox to the south terminal at Vancouver International Airport. It also provides service from Vancouver to Victoria, Nanaimo, Comox, Campbell River, Port Hardy, Powell River, Rivers Inlet, Hakai Pass, Bella Bella, Klemtu, Bella Coola, Anahim Lake, Dean River, Ocean Falls and other mid-coast communities.

"Westjet Airlines":http://www.westjet.com/home.html has daily service to Comox direct from Calgary.

"Westcoast Air":http://www.westcoastair.com/ has daily float plane service between the "Comox Bay Marina" (1805 Beaufort Avenue, Comox - phone: 250-339-2930) and Canada Place in Vancouver.


"Central Mountain Air":http://www.flycma.com/

|_. Toll: | 1 250 339-6900 |
|_. Toll-Free: | 1 800 663-3721 |

Small aircraft and float planes can land at Courtenay Airpark in downtown Courtenay.


h2. By Boat...

The newly expanded Comox Marina has every service nearby, including transient moorage, hot showers, laundry facilities, pubs, restaurants, shopping, marine repair, supplies and service.

"Comox Valley Harbour Authority":http://www.comoxfishermanswharf.com/

|_. Local | 1 250 339-6041 |

h3. Comox Bay Marina

|_. Local | 1 250 339-2930 |

h3. Black Fin Marina

|_. Local | 1 250 339-4664 |

h2. By Train...

The historic E & N Railway provides daily service between Victoria and Courtenay.

"E & N Railway (VIA Rail)":http://www.viarail.ca/

|_. Toll-Free | 1 800 561-8630 (in Canada) |
|_. Toll-Free | 1 800 561-3949 (in the USA) |
|_. Toll | 1 506 857-9830 (Call collect if not in Canada.) |""") ; _.save() ; _.attach(discover)


_ = Page(name="parks", title=u"Parks & Playing Fields", description=u"", content=u"""h1. Parks & Playing Fields

Located on the beautiful Comox Harbour in stunning natural scenery, Comox boasts many beautiful parks and relaxation areas.

*DID YOU KNOW....There are NO "_off leash_"* parks, fields or areas within the Town of Comox boundary* "(internal-link)Dog Licence and Pound Bylaw (Dog Licence and Pound Bylaw)":../town-hall/bylaws/Bylaw%201322%20Dog%20and%20Pound.pdf  - see bottom of page for more information.

To book a public park or ball field within the Town of Comox contact Comox Recreation Centre - phone: 250-339-2255.


h2. "Filberg Park":http://www.filberg.com/

is a stately home located on beautifully landscaped grounds a mere two minutes from down town Comox. Wander through the magnificent gardens, enjoy some refreshments at the Filberg Tea house or take the children to enjoy the Hands on Farm.

h2. Marina Park

is located right in the heart of town. This park offers a play area for children, a boat launch, washroom facilities and a covered picnic area with plenty of parking.

h2. Comox Promenade

offers a wonderful location to view the exhilarating scenery of the Comox Harbour and Beaufort Mountain Range. Spend an afternoon watching the sea life and activity in the Comox Harbour.

h2. Comox Golf Course

is located in the heart of down town Comox, offers nine holes of challenging golf all year round. Afterwards enjoy a meal or refreshments at the Club House.

h2. Anderton Park

is located next to the Comox Mall, offers six tennis courts, a basketball court, and playground equipment for the children. It is an excellent place to take children or play a game of tennis with your friends.


h2. Park Services

The tables below offer a summary of the facilities available at each location.

p(fl). !http://comox.ca/site-graphics/Parks2010.jpg!

table(hb-table).
| |_. Legend | |
|_. PT | Play Toys |
|_. Br | Bathrooms |
|_. Ta | Picnic Tables |
|_. Tr | Trails |
|_. Wd | Wooded |
|_. WF | Water Front |
|_. BT | Bicycle Trails |
|_. TC | Tennis Court |
|_. Bk | Basketball |
|_. Bs | Baseball |
|_. Vb | Volleyball |

table(cl grid matrix).
|_. Park |_.   |_. PT |_. Br |_. Ta |_. Tr |_. Wd |_. WF |_. BT |_. TC |_. Bk |_. Bs |_. Vb |
| Aspen          |  1 | • | • |   | • |   |   |   |   |   | 2 |   |
| Condor         |  2 |   |   |   | • | • |   |   |   |   |   |   |
| HarbourWood    |  3 |   | • |   |   |   |   |   |   |   |   |   |
| Pioneer        |  4 |   |   | • |   |   |   |   |   |   |   |   |
| Park Drive     |  5 |   |   |   |   |   |   |   |   |   |   |   |
| Port Augusta   |  6 |   |   |   |   |   | • |   |   |   |   |   |
| Marina         |  7 | • | • | • |   |   | • |   |   |   |   |   |
| Civic          |  8 |   |   |   |   |   |   |   |   |   |   |   |
| Anderton       |  9 | • | • |   |   |   |   |   | 6 | 1 |   |   |
| Filberg        | 10 |   | • | • |   |   | • |   |   |   |   |   |
| Brooklyn cr.   | 11 |   |   |   | • | • |   |   |   |   |   |   |
| Mack Laing     | 12 |   |   |   | • | • | • |   |   |   |   |   |
| MacDonald Wood | 13 |   |   |   | • | • | • |   |   |   |   |   |
| McKenzie       | 14 | • |   |   |   |   |   |   |   |   |   |   | 
| Village        | 15 | • |   | • |   |   |   |   | 2 | 1 | 2 |   |
| Tot Lot        | 16 | • |   |   | • | • | • |   |   |   |   |   |
| Salish         | 17 | • |   |   | • | • |   |   |   |   |   |   |
| Skeena         | 18 |   |   |   |   |   |   |   |   |   |   |   |
| N.E Comox      | 19 |   |   |   | • | • |   | • |   |   |   |   |
| Highland       | 20 |   | • |   |   |   |   |   |   |   | 3 |   |
| Foxxwood       | 21 |   |   |   | • | • |   |   |   |   |   |   |
| Highwood       | 22 |   |   |   |   |   |   |   |   |   |   |   |
| Golf Course    | 23 |   |   |   |   |   |   |   |   |   |   |   |
| Beckton        | 24 | • |   | • |   |   |   |   |   |   |   |   |
| Lancaster      | 25 |   |   |   |   |   |   |   |   |   |   |   |
| Queens         |    |   |   |   |   |   |   |   |   |   |   |   |
| Elks(Kye Bay)  |    | • | • | • |   |   | • |   |   |   |   |   |
| Promenade      |    |   |   | • |   |   |   |   |   |   |   |   |

* There are NO "*off-leash*" parks, fields or areas within the Town of Comox boundary - click this link for areas in the nearby *Comox Valley Regional District* for dogs to be "off-leash": "http://www.rdcs.bc.ca/uploadedFiles/Community_Services/Parks/Park_info/Leashing_Requirements.pdf":http://www.rdcs.bc.ca/uploadedFiles/Community_Services/Parks/Park_info/Leashing_Requirements.pdf
* Please keep our parks clean and respect fellow users by cleaning up after your pet. Here is a list of _*DOGGIE DOO STATION LOCATIONS*_ in Comox or stop by Town Hall for your complimentary bag:

p{text-align: center}.  

NORTH EAST WOODS – Torrence Avenue

COMOX VALLEY LION’S PARK – in Beckton Estates

MACDONALD WOOD PARK

CROTEAU ROAD  - beach access

MACK LAING PARK

COMOX MARINA – East and West side

COMOX HARBOUR AUTHORITY – building at beginning of pier walkway

ASPEN PARK

JANE PLACE – beach access

EDGEWATER PUB – walkway

PORT AUGUSTA PARK

ANDERTON PARK

FILBERG ROAD – beach access

LANCASTER PARK

SALISH PARK

ELKS & ROYAL PURPLE PARK – at Kye Bay

FORRESTER AVENUE - detention pond""") ; _.save() ; _.attach(discover)


_ = Page(name="filberg", title="Filberg Park & Lodge", description=u"", content=u"""h1. Filberg Park

p(fr). !http://comox.ca/site-graphics/filberg2page.jpg!

The Filberg Lodge and nine acres of beautifully landscaped grounds are located on the harbour near the end of Comox Avenue. The estate was originally built for R.J. Filberg in 1929, and became a public facility after his death in 1977. The Heritage Filberg Lodge and and Park Association (a non-profit society) manages and develops the property on behalf of the municipality.

p(cr). The rustic *Filberg Lodge* is a reflection of the skills of local craftsmen in the use of stone and timber. The original stonework was done by stone mason and head gardener William Meier. The Lodge's warm interior complements the outside appearance with extensive hand-made woodwork and stonework.

The *Gardens* are a myriad of exotic and local trees and flowers. A wonderful place for a peaceful stroll or an afternoon picnic.

The *Totem Pole* was created by Richard Krenz and donated by Gordon and Ivy Wagner. The totem pole features the crests of the four main families of the Comox native people.

The *Hands on Farm*, operated by the Town of Comox during the summer months, houses various farm animals. Admission is *free* for 5 years and under; *$2.00* for six years and older; *$5.00* for a family day pass and *$30.00* for a family season's pass. Admission is by* donation* during the Filberg Festival. (2005 rates)

The *Herb garden*, inviting to both the eye and the nose, is located just above the Tea House. The Garden was planted by the Comox Valley Horticultural Society.

The *Tea House*, open from May through September; (May 1, 11:00 a.m.-3:00 p.m. and starting in June the hours will increase to 11:00 a.m.-5:00 p.m.), offers morning coffee, lunches, and afteroon teas. The Tea House is situated in a restored outbuilding with a vine-covered patio and an excellent view. To reserve the Tea House call 339-1831.

h2. Filberg Festival

Each year the Filberg Festival is held in Comox to provide a four day forum for hundreds of artists and performers to display their work and entertain.

The festival is held each year in early August.  For this years dates visit %(link-external) "www.filbergfestival.com":http://www.filbergfestival.com/ %. Some of Canada's leading artists will be attending the festival to display their artwork and demonstrate their crafts. 

For more information about this years festival, including bio's of the featured artists, or the Filberg Estate in general, please visit the (link-external) "Filberg Heritage Lodge and Park Association ":http://www.filberg.com/ %web site, or contact the Coordinator:

| Phone | (250) 334-9242 |
| Fax | (250) 334-2899 |
| E-Mail | "info@filbergfestival.com":mailto:info@filbergfestival.com |"""
) ; _.save() ; _.attach(discover)


_ = Page(name="recreation", title=u"Recreation & Tourism", description=u"", content=u"""h1. Recreation & Tourism

Our Recreation Department Director calls Comox the Recreation Capital of BC (or was that Canada?) Take advantage of some of the fine accommodation that Comox has to offer. With the new Island Highway Comox is located approximately one hour away from Nanaimo. With many options on  "(external-link)how to get here":how-to-get-here  Comox is well worth incorporating into your vacation on Vancouver Island.

* Skiing
* Sailing
* Biking
* Canoeing
* Tennis
* Ball Diamonds
* Fishing
* Caving
* Gliding
* Community Centre
* Swimming
* Field Games
* Shooting
* Camping
* Hiking
* Golfing
* Skating
* Photography

The Comox Recreation Commission offers an average of 130 different recreational programs each quarter and some 40 special events each year, featuring arts programs, sports, recreation and culture. Whether your interest is gymnastics, arts & crafts, dance, racquet sports, basketball, soccer, yoga, sailing, general fitness, our weight room, badminton, or our hands-on farm, we're your recreation source in Comox! Be fit and have fun!

The modern facility offers gymnasiums, meeting rooms, squash and raquet ball courts, a well appointed weight room, showers and sauna. We even boast a kitchen with more than one sink!

Soccer pitches, baseball and softball diamonds, tennis courts and volleyball courts can all be booked here. Visit the "web site":http://comoxrecreation.com/ for all the details...


h2. Related Content

*"Comox Valley Tourism":http://comox.ca/links/comox* (An excellent site for both the visitor and resident highlighting things to do, see and experience around the Comox Valley.)
""") ; _.save() ; _.attach(discover)


links = Folder(name="links", title=u"Community Links", description=u"", default="view:details"); links.save() ; links.attach(discover)

# _ = Search(name="all", title=u"All Links", description=u"", query=u"kind:Alias", where=['/discover/links']) ; _.save() ; _.attach(links)
_ = Search(name="all", title=u"All Links", description=u"", query=u"tag:link", where=['/discover/links']) ; _.save() ; _.attach(links)

travel = Folder(name="travel", title=u"Travel", description=u"", default="view:details") ; travel.save() ; travel.attach(links)
tourism = Folder(name="tourism", title=u"Tourism", description=u"", default="view:details") ; tourism.save() ; tourism.attach(links)
accommodation = Folder(name="accommodation", title=u"Food and Accommodation", description=u"", default="view:details") ; accommodation.save() ; accommodation.attach(links)
recreation = Folder(name="recreation", title=u"Recreation", description=u"", default="view:details") ; recreation.save() ; recreation.attach(links)
community = Folder(name="community", title=u"Government and Community Services", description=u"", default="view:details") ; community.save() ; community.attach(links)
emergency = Folder(name="emergency", title=u"Emergency Contacts", description=u"", default="view:details") ; emergency.save() ; emergency.attach(links)

_ = Alias(tags=['link'], name="19-wing", title="19 Wing CFB Comox", description="Home page of 19 Wing CFB Comox.", target="http://www.airforce.forces.gc.ca/19w-19e/index-eng.asp") ; _.save() ; _.attach(community)
_ = Alias(tags=['link'], name="bc-ferries", title="BC Ferries", description="Up to date ferry departure and arrival information for all the routes in British Columbia.", target="http://www.bcferries.bc.ca/") ; _.save() ; _.attach(travel)
_ = Alias(tags=['link'], name="rental-assistance", title="BC Housing - Rental Assistance Program", description="The Rental Assistance Program was launched in October 2006 as part of Housing Matters BC. The program provides eligible low-income, working families with cash assistance to help with their montly rent payments.", target="http://www.bchousing.org/programs/RAP") ; _.save() ; _.attach(community)
_ = Alias(tags=['link'], name="bia", title="BIA (Comox Business in Action)", description="Comox Business in Action (BIA) \"Comox by the Sea\"", target="http://www.comoxbythesea.com/") ; _.save() ; _.attach(community)
_ = Alias(tags=['link'], name="green-building", title="Canada Green Building Council", description="Information on \"Green\" building standards, including LEED TM Certifications.", target="http://www.cagbc.ca/") ; _.save() ; _.attach(community)
_ = Alias(tags=['link'], name="can-mortgage", title="Canada Mortgage and Housing Corporation", description="CMHC offers a wide range of housing related information. Of particular interest is their \"Household Guide to Water Efficiency\".", target="http://www.cmhc-schl.gc.ca/") ; _.save() ; _.attach(community)
_ = Alias(tags=['link'], name="snow-birds", title="Canadian Forces Snowbirds", description="The Snowbirds are proud ambassadors of the men and women in Canada's military. They visit Comox each April for two weeks in preparation for their upcoming air show season.", target="http://www.snowbirds.forces.gc.ca/") ; _.save() ; _.attach(recreation)
_ = Alias(tags=['link'], name="mountain-air", title="Central Mountain Air", description="Central Mountain Air provides scheduled service between Vancouver (main terminal) and Campbell River-Comox.", target="http://www.flycma.com/") ; _.save() ; _.attach(travel)
_ = Alias(tags=['link'], name="9", title=u"Chamber of Commerce", description=u"""Comox Valley Chamber of Commerce                     """, target="http://www.comoxvalleychamber.com/") ; _.save() ; _.attach(community)
_ = Alias(tags=['link'], name="0", title=u"City of Courtenay", description=u"""The Comox Valley is made up of three municipalities, each with their own character. Our sister city of Courtenay can be found here.""", target="http://www.city.courtenay.bc.ca/") ; _.save() ; _.attach(community)
_ = Alias(tags=['link'], name="a", title=u"Comox Valley Tourism", description=u"""An excellent site for both the visitor and resident highlighting things to do, see and experience around the Comox Valley.                     """, target="http://www.discovercomoxvalley.com/") ; _.save() ; _.attach(tourism)
_ = Alias(tags=['link'], name="b", title=u"Comox Air Force Museum.", description=u"""The Comox Air Force Museum (CAFM), was founded in 1982 to reflect the role and history of 19 Wing (CFB/RCAF/RAF) Comox, the role and history of the Squadrons stationed here and significant aviators and aircraft of Western Canada                     """, target="http://www.comoxairforcemuseum.ca") ; _.save() ; _.attach(recreation)
_ = Alias(tags=['link'], name="c", title=u"Comox Archives & Museum Society", description=u"""The Comox Archives & Museum Society is located in downtown Comox. Every month there is a new display of interest to Comox Residents.                     """, target="http://www.comoxmuseum.ca/") ; _.save() ; _.attach(community)
_ = Alias(tags=['link'], name="d", title=u"Comox Golf Club", description=u"""Comox Golf Club is lovely semi-private nine hole golf course located in the heart of Comox, British Columbia. Our club is a leisurely walk from the Comox Marina, shopping, fine dining and pubs. We are only twenty minutes from the Comox Airport and Powell River ferry terminal.                      """, target="http://www.comoxgolfclub.com/") ; _.save() ; _.attach(recreation)
_ = Alias(tags=['link'], name="e", title=u"Comox Recreation", description=u"""Our separate recreation website, with information on recreation programs, services and faciltiies bookings.                     """, target="http://comoxrecreation.com") ; _.save() ; _.attach(recreation)
_ = Alias(tags=['link'], name="f", title=u"Comox Seniors' Centre Association", description=u"""The d'Esterre House Seniors' Centre was officially opened on June 25, 1975 by Lieutenant-Governor Walter Owen. The core group of 10 Senior Citizens has now grown to a membership of over 600.                     """, target="http://www.comoxseniors.ca/") ; _.save() ; _.attach(community)
_ = Alias(tags=['link'], name="g", title=u"Comox Tide Tables", description=u"""Link Fisheries & Oceans Canada website displaying tides for location # 7965 (Comox)                     """, target="http://www.waterlevels.gc.ca/cgi-bin/tide-shc.cgi?queryType=showFrameset&zone=13&language=english&region=1&stnnum=7965") ; _.save() ; _.attach(recreation)
_ = Alias(tags=['link'], name="h", title=u"Comox Valley Airport", description=u"""The Comox valley Airport is located in Comox,  within a three hour drive to most Vancouver Island locations.                     """, target="http://www.comoxairport.com/") ; _.save() ; _.attach(travel)
_ = Alias(tags=['link'], name="i", title=u"Comox Valley Arts Council", description=u"""For updates on speaker series and seminars being held through the Comox Valley Arts Council.                     """, target="http://www.comoxvalleyarts.org/") ; _.save() ; _.attach(recreation)
_ = Alias(tags=['link'], name="j", title=u"Comox Valley Emergency Prepardness Program", description=u"""Functions as a partnership between Comox, Courtenay, Cumberland and the regional district to provide coordinated emergency programming to the Comox Valley                     """, target="http://www.comoxvalleyrd.ca/section_comserv/content.asp?id=1689&collection=80") ; _.save() ; _.attach(emergency)



#_ = Page(name="", title=u"", content=u"""""") ; _.save() ; _.attach(discover)

_ = Page(name="album", title=u"Comox Album", description=u"", content=u"""h1. Welcome to the Town of Comox""") ; _.save() ; _.attach(discover)
_ = Page(name="deer", title=u"Expect Deer", description=u"", content=u"""h1. Expect Deer

p(fr). !http://comox.ca/site-graphics/expectdeersmall.jpg!

Expect deer on our roads and in your yard.

Visitors to Comox are often surprised to see deer wandering through our parks, greenways, streets and even private yards.

*Please observe our warning signs, expect deer, and drive carefully.*

Comox residents may have a different reaction to the presence of deer, particularly if the deer have been eating their way through gardens or orchards.

*Here are some thoughts about deer behaviour, and suggestions for dealing with troublesome deer in ways that do not hurt them:*

* An adult deer eats at least 3 kg of vegetation daily.  They need protein so they prefer legumes and sweet plants in rich well fertilized soil.  Berries, grains & fruit are also favourites.  Therefore substitute unsavoury plants for desirable ones or plant the edibles on the outside of your garden.
* Deer trust their noses, are curious, rely on habit, listen, and communicate with each other.  In a non-threatening environment (like Comox) they quickly learn that they are safe, and make themselves at home.
* Design your garden to discourage deer by creating uninviting entryways, and providing no view or landing sites (to fence leapers).  Mix preferred plant types with undesirable ones.  Consider using xeriscape landscaping (drought resistant plants) which generally are undesirable to deer.
* Be tidy and keep edible materials picked up (for instance fallen fruit).
* Deterrents to deer include foul smells (soap, hair, garlic, rotten eggs, and commercial compounds), movement (flags, scarecrows, or motion sensitive sprayers), floodlights or sounds (please be sensitive to your neighbours), and fencing (adult deer can jump a 2 metre high fence if they want to).  Remember that deer learn quickly that these deterrents are not really dangerous, so they only work for a while.
* Be considerate of your neighbours.  Don't use deterrents that irritate them more than the deer, and don't attract the deer to your neighbourhood by leaving out food.  Please remember that food will not only attract deer, but other animals, even less desirable.

Here are some links that may provide you with more ideas:

"When White-Tailed Deer Become a Nuisance (by Ross Hall)":http://www.gov.ns.ca/natr/wildlife/nuisance/deer.asp


h2. Related content

"*Deer Resistant Plant List 1*"::http://comox.ca/town-hall/other-documents/plants-deer-usually-do-not-eat.pdf/view (This is a listing we found of plants that deer usually do not eat (in pdf format).
"*Deer Resistant Plant List 2*":http://comox.ca/town-hall/other-documents/the-following-plants-are-rarely-damaged-by-deer-according.pdf/view (This a listing of plants rarely damaged by deer obtained from the Art Knapp Plantland Website, in Adobe Acrobat (pdf) format.)
""") ; _.save() ; _.attach(discover)

# redirect old page bookmarks to new location after moving/renaiming content
_ = Alias(name="gethere", title="", target="/discover/directions") ; _.save() ; _.attach(discover)
_ = Alias(name="rec-tour", title="", target="/discover/recreation") ; _.save() ; _.attach(discover)


events = Folder(name="events", title=u"Community Events", description=u"", default="view:details") ; events.save() ; events.attach(discover)

event = Event(
        name = "bob-lunch",
        title = u"Lunch with Bob",
        content = u"""This is a description...""",
        starts = datetime(2010,10,1,12,0),
        stops = datetime(2010,10,1,13,0),
        organizer = u"Top Floor Computer Systems Ltd.",
        location = u"1765 Fern Road, Courtenay, BC",
        contact = EventContact(name=u"Howard Bevan", email="webmaster@topfloor.ca", phone="250 898-8783")
    ) ; event.save() ; event.attach(events)

_ = Page(name="hmcs", title=u"HMCS Comox", description=u"", content=u"""h1. Welcome to the Town of Comox""") ; _.save() ; _.attach(discover)


hall = Folder(name="hall", title=u"Town Hall", description=u"", default="default") ; hall.save() ; hall.attach(root)
_ = Page(name="default", title=u"Town Hall", description=u"", content=u"""h1. Town Contact Information
    
*The Town of Comox has seven departments, each with their own area of responsibility. The table below contains information that will help you contact the right department and person, to assist you with any inquiry you may have.*
    
h2. Administration - Town Hall

The Town of Comox Town Hall is the administrative center of the town. Inquiries regarding Council, Public Meetings, and Bylaws should be directed here.

<dl class="hb-col"><dt>Address:</dt><dd>Town Hall<br />1809 Beaufort Ave.<br />Comox, B.C.<br />V9M 1R9</dd></dl>
<dl class="hb-col"><dt>Administrator:</dt><dd>Richard Kanigan</dd><dt>Business:</dt><dd>(250) 339-2202</dd><dt>Fax:</dt><dd>(250) 339-7110</dd></dl>
<dl class="hb-col"><dt>Deputy Corp. Admin.:</dt><dd>Shelly Russwurm</dd><dt>Business:</dt><dd>(250) 339-2202</dd><dt>Fax:</dt><dd>(250) 339-7110</dd></dl>

h2. Finance

The Finance Department is responsible for budgets, collections, and financial reporting. It issues tax notices, utility billings, invoices, and business licence renewals. It also deals with the Municipal Marina. For more information on finance, taxes, or charges for Town services, click the link here: <a href="departments/finance-department/" target="_self">Finance Page</a>

<dl class="hb-col"><dt>Director of Finance:</dt><dd>Donald Jacquest</dd><dt>Business:</dt><dd>(250) 339-2202</dd><dt>Fax:</dt><dd>(250) 339-7110</dd></dl>

h2. Building Department

The Building Department oversees the issuing of building permits and assures compliance with the building codes, regulations and by-laws of both the Province and the Town of Comox.

<dl class="hb-col"><dt>Inspectors:</dt><dd>Trevor Roberts & Gig Morton</dd><dt>Business:</dt><dd>(250) 339-2259</dd><dt>Fax:</dt><dd>(250) 339-7110</dd><dt>Address:</dt><dd>Lower Floor, Town Hall<br />1809 Beaufort Ave.<br />Comox, B.C.     V9M 1R9</dd></dl>

h2. Fire Department

The Comox Fire Department provides a variety of preventative and emergency services to the Town of Comox, the Comox Fire Protection Improvement District, the Bates/Huband Local Service Area and the Comox Indian Band.

These services include fire safety inspections and consultations, smoke alarm installation and testing, fire and burn safety education, firefighting, rescue, assessing and limiting exposure to hazardous material leaks and spills as well as first responder assistance to BC Ambulance Service and BC Forest Service.

The Comox Fire Department is staffed by three full-time and fourty paid-on-call employees. Their fleet includes two engines, one ladder truck, two rescue vehicles, one fireboat and one staff vehicle.

For more information, including descriptions of all the services offered, click <a href="departments/comox-fire-department/">here.</a>

<dl class="hb-col"><dt><strong>Emergency:</strong></dt><dd><strong>911</strong></dd></dl>
<dl class="hb-col"><dt>Chief:</dt><dd>Gord Schreiner</dd><dt>Business:</dt><dd>(250) 339-2432</dd><dt>Fax:</dt><dd>(250) 339-1988</dd><dt>Address:</dt><dd>Comox Fire Department<br />1870 Noel Avenue<br />Comox, B.C.     V9M 2K9</dd></dl>

h2. Parks Department

The Parks Department is responsible for keeping Comox beautiful, at least horticulturally. Playing fields, Parks and road allowances all fall under their jurisdiction.

<dl class="hb-col"><dt>Superintendent:</dt><dd>Allan Fraser</dd><dt>Business:</dt><dd>(250) 339-2421</dd><dt>Fax:</dt><dd>(250) 339-7110</dd><dt>Delivery Address:</dt><dd>Works Yard<br />1390 Guthrie Road<br />Comox, B.C.     V9M 0A5</dd></dl>

h2. Planning Department

The Planning Department is responsible for the Town's Official Community Plan, Zoning Bylaws and the processing of land development applications including development permits, development variance permits and subdivisions.

<dl class="hb-col"><dt>Address:</dt><dd>Town Hall<br />1809 Beaufort Ave.<br />Comox, B.C.     V9M 1R9</dd></dl>
<dl class="hb-col"><dt>Municipal Planner:</dt><dd>Marvin Kamenz</dd><dt>Business:</dt><dd>(250) 339-1118</dd><dt>Fax:</dt><dd>(250) 339-7110</dd></dl>
<dl class="hb-col"><dt>Planner II:</dt><dd>Gail Andestad</dd><dt>Business:</dt><dd>(250) 339-1118</dd><dt>Fax:</dt><dd>(250) 339-7110</dd></dl>
<dl class="hb-col"><dt>Planner I:</dt><dd>Peter Marohnic</dd><dt>Business:</dt><dd>(250) 339-1118</dd><dt>Fax:</dt><dd>(250) 339-7110</dd></dl>

h2. Public Works

The Public Works Department look after the town infrastructure. This includes the water, sewer and drainage system and road surfaces for which the town is responsible.

<dl class="hb-col"><dt>Superintendent:</dt><dd>Glenn Westendorp</dd><dt>Business:</dt><dd>(250) 339-5410</dd><dt>Fax:</dt><dd>(250) 890-0698</dd><dt>Delivery Address:</dt><dd>Public Works Yard<br />1390 Guthrie Road<br />Comox, B.C.     V9M 0A5</dd></dl>
""") ; _.save() ; _.attach(hall)


announcements = Folder(name="announcements", title=u"Announcements", description=u"", default="view:details", sort="-created") ; announcements.save() ; announcements.attach(hall)


bylaws = Folder(name="bylaws", title=u"Bylaws", description=u"", default="view:details", sort="created") ; bylaws.save() ; bylaws.attach(hall)
_ = Page(name="departments", title=u"Departments", description=u"", content=u"""h1. Departments
    
*Comox Town Hall has six departments, each with their own areas of responsibility.*

<img class="image-left" src="http://comox.ca/site-graphics/OrgChart.jpg" alt="Organization Chart" height="206" width="660" /></p>

Each Department is headed by a Manager. The Administrator and the Manager of each Department make up the Senior Management Team, which meets regularly to discuss operational issues of the Town. Team members identify potential solutions and make recommendations to Council on the various issues faced by each Department.

|_. DEPARTMENT |_. LOCATION |_. MANAGER |_. PHONE |
| <a href="administration/">*Corporate Administration*</a> | 1809 Beaufort Avenue | Shelly Russwurm | 339-2202 |
| <a href="finance-department/">*Finance*</a></strong> | 1809 Beaufort Avenue | Donald Jacquest | 339-2202 |
| <a href="comox-fire-department/">*Fire*</a></strong> | 1870 Noel Avenue | Gord Schreiner | 339-2432 |
| <a /services/parks/">*Parks &Facility Maintenance*</a> | 1390 Guthrie Road | Al Fraser | 339-2421 |
| <a href="planning-and-building">*Planning & Building Inspection*</a> | 1809 Beaufort Avenue | Marvin Kamenz | 339-1118 |
| *Public Works* | 1390 Guthrie Road | Glenn Westendorp | 339-2202 |

""") ; _.save() ; _.attach(hall)
meetings = Folder(name="meetings", title=u"Meetings", description=u"", default="view:details") ; meetings.save() ; meetings.attach(hall)

agendas = Folder(name="agendas", title=u"Agendas", description=u"", default="view:details", sort="-created") ; agendas.save() ; agendas.attach(meetings)
minutes = Folder(name="minutes", title=u"Minutes", description=u"", default="view:details", sort="-created") ; minutes.save() ; minutes.attach(meetings)
_ = Page(name="cm-dates", title=u"2010 Council Meeting Dates", description=u"", content=u"""h1. PUBLIC NOTICE

In accordance with Section 127 of the Community Charter the following is a schedule of Regular Council meetings and Committee of the Whole meetings to be held during 2010.

h2. REGULAR COUNCIL MEETINGS - 2010

Regular Council Meetings are scheduled for the first and third Wednesday of each month, commencing at 5:30 p.m. Amendments have been made to allow for summer holidays and conference schedules. Meetings will be held in the Council Chambers located at 1801B Beaufort Avenue. The specific dates of the Regular Council meetings are as follows:

|  | JANUARY 20 |
| FEBRUARY 03 | FEBRUARY 17 |
| MARCH 03    | MARCH 17 | 
| APRIL 07    | APRIL 21 |
| MAY 05      | MAY 19 |
| JUNE 02     | JUNE 16 |
|             | JULY 21|
|             | AUGUST 18 |
| SEPTEMBER 01 | SEPTEMBER 15 |
| OCTOBER 06  | OCTOBER 20 |
| NOVEMBER 03 | NOVEMBER 17 |
| DECEMBER 01 | DECEMBER 15 |

h2. COMMITTEE OF THE WHOLE MEETINGS - 2010
 
Committee of the Whole meetings are scheduled for the second and fourth Wednesday of each month, commencing at 4:15 p.m. Amendments have been made to allow for summer holidays and conference schedules. Meetings will be held in the Council Chambers located at 1801B Beaufort Avenue. The specific dates of the Committee of the Whole meetings are as follows:

| JANUARY 13  | JANUARY 27 |
| FEBRUARY 10 | FEBRUARY 24 |
| MARCH 10    | MARCH 24 |
| APRIL 14    | APRIL 28 |
| MAY 12      | MAY 26 |
|             | JUNE 23 |
| SEPTEMBER 08 | SEPTEMBER 22 |
| OCTOBER 13   | OCTOBER 27 |
| NOVEMBER 10  | NOVEMBER 24 |
| DECEMBER 08  |            |
      
If you require additional information, please feel free to contact staff at Comox Town Hall at (250) 339-2202.

A copy of this notice is available at Comox Town Hall, 1809 Beaufort Avenue. In addition, the schedule of meetings can also be found on the Town website: www.comox.ca"""); _.save() ; _.attach(meetings)

news2 = Page(name="news2", title=u"Foo Bar Baz", tags=['news'], description=u"Lorem ipsum dolor sit amet, consectetur adipisicing elit", content=u"""It's the end of the world and I feel fine.""") ; news2.save() ; news2.attach(root)
news1 = Page(name="news1", title=u"End of the World Nigh", tags=['news'], description=u"This just in, it's the end of the world.", content=u"""It's the end of the world and I feel fine.""") ; news1.save() ; news1.attach(root)
news3 = Page(name="news3", title=u"Diz Bat Bar", tags=['news'], description=u"Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", content=u"""It's the end of the world and I feel fine.""") ; news3.save() ; news3.attach(root)

_ = Page(
        name = "remove-boil",
        title = u"Removal of Boil Water Notice",
        description = u"""Effective September 13, 2010 the Comox Valley Regional District and the Vancouver Island Health Authority are removing the boil water notice for the users of the Comox Valley Water System.""",
        content = u"""h1. Removal of Boil Water Notice
        
*Effective September 13, 2010 the Comox Valley Regional District and the Vancouver Island Health Authority are removing the boil water notice for the users of the Comox Valley Water System.*

The boil water advisory has been removed from the Comox Valley Water System because three complete sets of satisfactory water tests have been received since a single sample in last week’s set of regular Regional District water tests was positive for e-coli bacteria. The Town’s water is now safe to use for all purposes.

After a boil water notice is ended, you are recommended to you run cold water faucets and fountains for 1 minute before using the water, to drain and flush ice making machines, to run water softeners through a regeneration cycle, to drain and refill hot water tanks if they are less than 45 degrees celcius in temperature (normal is 60 degrees), and to change any water pre-treatment filters that you use.

h2. Background

Comox (along with the City of Courtenay and several Electoral Area water systems) buys its drinking water from the Regional District. The Regional District’s water originates at Comox Lake, although the water is drawn from the BC Hydro penstock for most of the year, except when the penstock is being maintained, at which time it is drawn from the Puntledge River beside the BC Hydro generating station. The Regional District checks the water taken for turbidity, and then adds chlorine for purification. It takes six water samples from downstream locations through its water system weekly. Last week one of those samples (from the Arden Road water system) tested positive for e-coli bacteria, and so the boil water notice was issued for the whole of the Regional water system.

In addition to the testing that the Regional District performs, the Town of Comox takes five water samples per week from locations around Comox. We have yet to have a sample test positive for e-coli in Comox. And in addition to scheduled testing by the Regional District and the Town, the Vancouver Island Health Authority takes water samples at random to verify the work we are performing.

For additional information on water testing and water quality, please note the related item links below.

We appreciate the co-operation of the public with the boil water advisory that was issued last week. And while there was no evidence of widespread contamination in the Regional water system or in Comox, the boil water notice was issued out of caution, because there was a small chance that could occur. Our staff will continue to act to preserve the security of our water, and protect public health."""
) ; _.save() ; _.attach(announcements)
    
    
_ = Page(
        name = "knight-road",
        title = u"Knight Road Closure",
        description = u"""Knight Road Sanitary Sewer Project Extension.""",
        content = u"""h1. Knight Road Sanitary Sewer Project Extension

p(fr). <img src="http://comox.ca/news-items/knight-road-closure/image" width="200">

Please be advised that starting *October 18, 2010 - November 15, 2010*, J.R. Edgett Excavating Ltd. will be starting work on an infrastructure upgrade on Knight Road, west of the Pritchard Road intersection.

Please be aware of temporary signage and detours and follow all instructions from traffic control personnel.  For further info contact J.R. Edgett Exc. Ltd. at 250-339-6100."" """
) ; _.save() ; _.attach(announcements)

_ = Page(name="by-election", title=u"Municipal By Election", description=u"", content=u"""h1. 2011 Councillor By-Election

*A by-election will be held on Saturday, January 15, 2011 to elect one Councillor to serve the remainder of the current three-year term of December 2008 through December 2011. Please watch this webpage and local newspapers for further information.*
 

h2. VOTING OPPORTUNITIES:

Council appointed Richard Kanigan as Chief Election Officer effective October 27th, 2010 and he has set the General Voting Day as *Saturday, January 15, 2011*. There will also be two Advance Voting Opportunities to take place on: Jan 5th and Jan 12th, 2011.

For additional information watch for the NOTICE OF ELECTION BY VOTING to appear in the RELATED ITEMS section below.

 

h2. NOMINATION PERIOD:

Will begin at 9:00 am on *Tuesday, November 30th* till 4:00 pm on Friday, December 10th, 2010.

For additional information watch for the NOTICE OF NOMINATION to appear in the RELATED ITEMS section below.
""") ; _.save() ; _.attach(root)


services = Folder(name="services", title=u"Municipal Services", description=u"", default="view:details") ; services.save() ; services.attach(root)
#_ = Page(name="default", title=u"Municipal Services", description=u"", content=u"""h1. Welcome to our Municipal Services""") ; _.save() ; _.attach(services)

_ = Page(name="bus-licence", title=u"Business Licensing", description=u"This is the business licence description", content=u"""h1. Business Licensing

All businesses, including home-based businesses, operating within the Town of Comox require a business licence. Business licences are valid for each calendar year period, and can be applied for at any time throughout the year. For more information on operating a business in the Town of Comox, please see the Comox Business Licence Bylaw .

NEW! Effective 2007, the Town of Comox has entered into an Intermunicipal Business Licence Agreement with the City of Courtenay allowing certain businesses that operate in both communities the option of purchasing a single licence. For more information on this program, please see the Intermunicipal Business Licence Bylaw and Agreement or call Town Hall at 250 339-2202.

The Town of Comox also has a partnership agreement with *OneStop Business Registry*, which offers integrated business registry services. If you are starting up a new business or wish to change the address of your business, you can use the OneStop service to register with many of the federal, provincial and local government agencies all in one step.

To apply for a Town of Comox Business Licence, either directly with the Town or through the OneStop Business Registry, use one of the links below:

<img border="0" width="65" height="65" src="http://comox.ca/site-graphics/admin/BlueBoat.JPG" alt="OneStop" /></a> Comox Business Licence Application

!http://comox.ca/site-graphics/admin/OneStop.jpg! OneStop Business Registry Service""", default="view:details") ; _.save() ; _.attach(services)

_ = Page(name="recycling", title=u"Recycling and Garbage - 2010", description=u"A summary of our recycling initiatives.", content=u"""h1. Recycling and Garbage for 2010

*A summary of our services.*

h2. Residential Yard Waste Collection:

!>http://comox.ca/site-graphics/YardWaste.jpg/image_mini!

Weekly collection from single-family homes & duplexes

(on garbage day all year round)

* Grass, plants, flowers, leaves, sod and small amounts of soil in special 100% compostable or 100% biodegradable plastic or paper yard waste bags that have been individually marked as such by the manufacturer and do not exceed 77 litres in volume or 20 kilograms (44 pounds) in weight.

* You may also use garbage cans (with lids on) that are marked clearly as “Yard Waste” and do not exceed 77 litres in volume or 20 kilograms (44 pounds) in weight.

* Tree prunings, hedge prunings and branches must be tied in secure bundles no longer than 90 cm. (36 in.) or wider than 60 cm. (24 in.) in diameter, or heavier than 20 kg. (44 lb.). Individual branches must not exceed 7.6 cm (3 in.) in diameter.

* Christmas trees – cut in half with no tinsel or decorations are treated as branches.

* *NO LIMITS ON QUANTITY OF YARD WASTE*

* You may NOT include rocks, stumps, flower pots, painted or treated wood, animal feces, kitchen waste, garbage or recyclables with your yard waste

* Have your yard waste at the curb by 8 am to ensure that the contractor will pick it up

* Please call our garbage collection contractor Emterra at 250-336-8066 if you have questions about their service.

h3. Residential Blue Box Recycling:

Residential pickup of recycling continues bi-weekly in 2010. For full details consult our __COMOX RECYCLES GUIDE__ under related items at bottom of this page.

h4. CHANGE FROM BLUE BAGS TO BLUE BOXES:

The use of BLUE BAGS for recycling has been phased out and replaced with a BLUE BOX system - starting on January 1, 2009 blue bags were no longer collected. At the start of this program one blue box was distributed to each single family home and duplex in Comox on a one-time basis.  This blue box became the private property of the property owner.  You must have at least one blue box to take part in the program. Click here for some reasoning behind the Change from BLUE BAGS to BLUE BOXES and HOW TO PURCHASE ONE.

h4. HOW TO USE THE BLUE BOX:

Please place mixed (unsorted) recyclables into the blue box (just as you used to in the blue bag), however do not place a paper product inside a plastic product - such as shredded paper inside a plastic bag - instead put paper inside paper such as shredded paper inside a paper bag or cardboard box. Plastic shopping bags and plastic wrap can now be added to the mixed recyclabels, if clean.

h4. NO GLASS!  NO STYROFOAM!  We cannot recycle these.

If your blue box is full, extra recyclables can be placed in any other open container next to the blue box -ensure that these additional containers do not exceed the basic dimensions of the blue box and remember the weight limit on all containers of 35 pounds - *NO LIMITS ON RECYCLING QUANTITIES*.

Click here for TIPS on Packing your Blue Box for a windy day.

* Have your recycling at the curb by 8 am to ensure that the contractor will pick it up

* Please call our garbage collection contractor Emterra at 250-336-8066 if you have questions about their service.
2010 pickup Dates: 
(Tuesday - Friday)


|JAN. |2, 12-15, 26-29 |
|FEB. |9-12, 23-26 |
|MARCH |9-12, 23-26|
|APRIL |6-9, 20-23|
|MAY |4-7, 18-21!
|JUNE |1-4, 15-18, 29 & 30|
|JULY |1-2, 13-16, 27-30|
|AUG. |10-13, 24-27|
|SEPT. |7-10, 21-24|
|OCT. |5-8, 19-22|
|NOV. |2-5, 16-19 & 30|
|DEC. |1-3, 14-17, 28-31|


h4. USE YOUR BLUE BOX FOR:

* Plastic Milk Jugs
* Plastic Containers (types 1-7)
* Metal Food Containers
* Mixed Paper
* Cardboard
* *NO Glass*
* *NO Styrofoam*


h3. Residential Garbage Collection:

* Weekly Pickup – see map and schedule in Comox Recycles Guide (below)
* Maximum one 121 litre garbage can starting in 2007
* Additional can over limit will only be picked up if a garbage tag is attached These can be purchased from Town Hall (1809 Beaufort Avenue) for $2.40 each (no tax)
* Must use cans with secure waterproof lids Cans cannot exceed 20 kilograms (44 pounds)
* NO yard waste allowed with garbage (see yard waste collection details above)
* NO demolition or construction material allowed  You can take these materials directly to the Regional District’s Pidgeon Lake Landfill
* Have your garbage at the curb by 8 am to ensure that the contractor will pick it up
* Please call our garbage collection contractor Emterra at 250-336-8066 if you have questions about their service.
 

h3. Other Recycling in Comox:
 
"Comox Return Centre":http://www.encorp.ca/cfm/index.cfm?It=101&Se=38 678 Anderton Road (339-0059)

Provides refunds for all beverage containers including juice, water, pop, wine, and spirits sold in plastic, metal, glass or Tetra pack containers. Please rinse and remove lids, but leave labels on. In addition, this is the Comox Valley’s Paint and Paint Products return centre.

"Comox Valley Regional District Recycling Depots":http://www.comoxstrathcona.ca/section_comserv/content.asp?id=91&collection=80

Depots for depositing plastic milk jugs, metal, glass and plastic (types 1-7) food containers, mixed paper (newspapers, magazines, junk mail, phone books) cardboard, and boxboard. No Styrofoam. Depots are located adjacent to:

* Canex (CFB Comox)
* Comox Centre Mall (Downtown)
* Quality Foods (2275 Guthrie Road)
* Home Depot, Ryan and Lerwick, Courtenay

* Encorp Return-It Electronics at the Courtenay Return Centre - phone: 250-338-6013 Certain old computers, monitors, printers, fax machines & televisions.

* Journey Recycling Program: 250-338-5884 - picks up office paper. 

* "Recycling Council of British Columbia (RCBC)":http://rcbc.bc.ca/ - lets you search by product material and your location.

* Recycling Hotline 1-800-667-4321

 

h4. Regional Landfill

The Comox Valley Waste Management Centre is located near the Village of Cumberland. For further information on the Landfill please call the Comox Valley Regional District at 250-334-6000.

h4. Related content

Comox Waste Collection Guide 2010-2011""") ; _.save() ; _.attach(services)

marina= Folder(name="marina", title=u"Comox Bay Marina", description=u"Planning Documents related to OCP RZ 06-13 & DP 06-12; 1803, 1805 & 1823 Beaufort Ave, 127 Port Augusta Street and Block A, District Lot 380, Nanaimo District", content=u"""Comox Bay Marina
Planning Documents related to OCP RZ 06-13 & DP 06-12; 1803, 1805 & 1823 Beaufort Ave, 127 Port Augusta Street and Block A, District Lot 380, Nanaimo District""") ; _.save() ; _.attach(services)

_ = Page(name="maps", title=u"Maps", description=u"All of the maps on the site can be found here. Some are simple images, others full colour detailed maps in Adobe PDF format, and will require an external reader available from Adobe.", content=u"""h1. Welcome to Comox Maps""") ; _.save() ; _.attach(services)

_ = Page(name="parks", title=u"Municipal Parks", description=u"Map showing park locations and table of park amenities.", content=u"""h1. Welcome to Comox Parks""") ; _.save() ; _.attach(services)
_ = Page(name="works", title=u"Public Works", description=u"Structures, functions and services of the Public Works Department", content=u"""h1. Welcome to Public Works""") ; _.save() ; _.attach(services)
_ = Page(name="conservation", title=u"Water Conservation", description=u"The Town, as a customer of the Comox Valley water system, is subject to the water use restrictions enacted by the Comox Valley Regional District. Since 2006 there have been year-round restrictions on sprinkling. These were recently updated when the Comox Valley Regional District adopted a new bylaw (No. 129).", content=u"""h1. Water Conservation

The Town, as a customer of the Comox Valley water system, is subject to the water use restrictions enacted by the Comox Valley Regional District. Since 2006 there have been year-round restrictions on sprinkling. These were recently updated when the Comox Valley Regional District adopted a new bylaw (No. 129).
This Regional District Bylaw No. 129 (see Related Content box at bottom of page) has a three-stage water conservation program. Restrictions apply year-round starting with Stage 1.  Stage 2 will generally be in effect from June 1 until September 30th, but can be implemented earlier and maintained later if required. And Stage 3, the most restrictive level of water use, is imposed as required based upon water availability and demand.  The public will be notified of the change to Stage 2 or 3 through the local newspaper and radio or you may wish to phone a local municipal hall or visit a website - see the Contact Information at the bottom of this page.

Please note, that although this is a Regional District Bylaw it can be enforced by bylaw enforcement officers from both the Town of Comox and the Regional District. If you wish to report a non-compliance, within the Town's boundary, please contact Comox Town Hall and be prepared to provide the address of concern.

Should you have concerns about the restrictions within the Bylaw itself please contact the Comox Valley Regional District office directly at 250-334-6000.

h2. Stages 1, 2 and 3 (summary only):

Click on the *"RELATED CONTENT"* box below for details

*NOTE:* If you live in a multi-unit building then during stages 1 and 2 the word "address" means the main mailing address for your building - NOT the individual building's unit numbers.

h3. STAGE 1 - EVEN / ODD DAYS SPRINKLING

People living at an even numbered address may only use a sprinkler to water a lawn on an even numbered date, from 4:00 a.m. to 9:00 am in the morning and 7:00 p.m. to 10:00 pm in the evening.
People at at an odd numbered address may only use a sprinkler to water a lawn on an odd numbered date, from 4:00 a.m. to 9:00 am in the morning and 7:00 p.m. to 10:00 pm in the evening.

h3. STAGE 2 - SPECIFIC DAYS IN WEEK FOR SPRINKLING

People living at an even numbered address may only use a sprinkler to water a lawn on Tuesday and Saturday from 4:00 a.m. to 9:00 am in the morning and 7:00 p.m. to 10:00 pm in the evening.

People at an odd numbered address may only use a sprinkler to water a lawn on Wednesday and Sunday from 4:00 a.m. to 9:00 am in the morning and 7:00 p.m. to 10:00 pm in the evening.

No person may use water to wash sidewalks, driveways, and parking lots except as necessary for applying a product such as paint, preservative and stucco, preparing a surface prior to paving or repointing bricks, or if required by law to comply with health or safety regulations.

h3. STAGE 3 - NO LAWN SPRINKLING

No one may water a lawn or boulevard; fill or add water to a swimming pool, hot tub, or garden pond; fill or add water to or operate a decorative fountain at any time; or wash a vehicle or a boat with water.
FOR TIPS ON CONSERVING WATER IN THE YARD PLEASE CLICK ON THE LINK BELOW

"Water Wise":http://comox.ca/town-hall/other-documents/TIPS%20FOR%20CONSERVING%20WATER%20IN%20THE%20YARD.pdf/attachment_download/file

h2. Exceptions and Enforcement (summary only):

 Click on the *"RELATED CONTENT"* box below for details

There are some exceptions to the bylaw... 

A LAWN SPRINKLING PERMIT ($30.00 fee) is available from the Town of Comox for people who have installed a new lawn, either with sod or with grass seed.  These permits make it possible (during Stage 1 and 2 ONLY) for people to water their new lawn outside of permitted days, but still within the restricted hours for a set number of days. 

As well, there are other specific exceptions for nurseries, farms, golf courses and public authorities - such as the Playing Field Exemption

The bylaw is in place all year long but will be strictly enforced during June to September, when residential water use is highest.  Enforcement of the bylaw will be coordinated by the Town of Comox bylaw enforcement officer who is able to issue fines to people who do not comply.

Click to return to the Town of Comox website's "HOME PAGE":/

h3. Contact Information:

Comox Valley Regional District:             
Phone: 250-334-6000                                    
Website: www.comoxvalleyrd.ca (click on the Water Info drop in the top/middle of the home page)                 

   

*Town of Comox:*

Phone: 250-339-2202

Website: comox.ca (click on the Water Stage box at the bottom of the home page)

*Related content*

Water Conservation Detailed Regulations
CVRD Bylaw No. 129 - (Full)""") ; _.save() ; _.attach(services)

_ = Page(name="sewer", title=u"Sewer", description=u"", content=u"""h1. Welcome to Comox Sewer""") ; _.save() ; _.attach(services)

_ = Page(name="recreation", title=u"Comox Recreation Centre", description=u"We offer an average of 130 different recreational programs each quarter and some 40 special events each year, featuring arts programs, sports, recreation and culture.", content=u"""h1. Welcome to Comox Recreation Centre""") ; _.save() ; _.attach(services)

_ = Page(name="finance", title=u"Finance Department", description=u"The Finance Department is responsible for budgets, collections, and financial reporting. We issue tax notices, utility billings, invoices, business licence renewals, and invoices for the Municipal Marina. The related item links below are documents that are of interest to the public. If you have questions about them, please contact the Finance Department.", content=u"""h1. Welcome to Comox Finance Department""") ; _.save() ; _.attach(services)

interactive = Folder(name="interactive", title=u"Interactive", description=u"", default="view:details") ; interactive.save() ; interactive.attach(root)
#_ = Page(name="default", title=u"Interactive", description=u"", content=u"""h1. Welcome to Comox Interactive""") ; _.save() ; _.attach(interactive)

_ = Page(name="feedback", title=u"Feedback", description=u"", content=u"""h1. Welcome to Comox Feedback""") ; _.save() ; _.attach(interactive)

_ = Page(name="blog", title=u"Comox Herald (blog)", description=u"", content=u"""h1. Welcome to Comox Herald (blog)""") ; _.save() ; _.attach(interactive)

questions = Folder(name="questions", title=u"Questions and Answers", description=u"", default="view:details") ; questions.save() ; questions.attach(interactive)

general = Folder(name="general", title=u"General Questions and Answers", description=u"", default="view:details") ; general.save() ; general.attach(questions)

animals = Folder(name="animals", title=u"Animals Questions and Answers", description=u"", default="view:details") ; animals.save() ; animals.attach(questions)
_ = Page(name="Q01", title=u"h1. Q. Are there any \"off leash\" parks or areas in the Town of Comox?", description=u"", content=u'''h1. Q:  Are there any "off leash" parks or areas in the Town of Comox?

There are *NO* "off-leash" parks, fields or areas within the Town of Comox boundary - click "this link":http://www.rdcs.bc.ca/uploadedFiles/Community_Services/Parks/Park_info/Leashing_Requirements.pdf for areas in the nearby Comox Valley Regional District for dogs to be ""off-leash"''') ; _.save() ; _.attach(animals)
_ = Page(name="Q02", title=u"h1. Q. Where are the Doggy Dog Bag Stations in Comox?", description=u"", content=u'''h1. Q: Where are the Doggy Dog Bag Stations in Comox?
 

Please keep our parks clean and respect fellow users by cleaning up after your pet. Here is a list of DOGGIE DOO STATION LOCATIONS  in Comox or stop by Town Hall for your complimentary bag:

*NORTH EAST WOODS – Torrence Avenue
*COMOX VALLEY LION’S PARK – in Beckton Estates
*MACDONALD WOOD PARK
*CROTEAU ROAD  - beach access
*MACK LAING PARK
*COMOX MARINA – East and West side
*COMOX HARBOUR AUTHORITY – building at beginning of pier walkway
*ASPEN PARK
*JANE PLACE – beach access
*EDGEWATER PUB – walkway
*PORT AUGUSTA PARK
*ANDERTON PARK
*FILBERG ROAD – beach access
*LANCASTER PARK
*SALISH PARK
*ELKS & ROYAL PURPLE PARK – at Kye Bay
*FORRESTER AVENUE - detention pond
''') ; _.save() ; _.attach(animals)

_ = Page(name="Q03", title=u"h1. Q. Who do I call if I have a complaint about a dog?", description=u"", content=u'''h1. Q. Who do I call if I have a complaint about a dog?
 
Call the SPCA at phone: 250-339-7722 &/or the Town of Comox Bylaw Enforcement Officer at phone: 250-339-2202."''') ; _.save() ; _.attach(animals)

garbage = Folder(name="garbage", title=u"Garbage, Recyling and Yard Waste Questions and Answers", description=u"", default="view:details") ; garbage.save() ; garbage.attach(questions)


_ = Page(name="tax-search", title=u"Feedback", description=u"", content=u"""h1. Welcome to Comox Feedback""") ; _.save() ; _.attach(interactive)

_ = Page(name="homegrant", title=u"Home Owner Grant", description=u"", content=u"""h1. Welcome to Home Owner Grant""") ; _.save() ; _.attach(interactive)

forms = Folder(name="forms", title=u"Application Forms", description=u"", default="default") ; forms.save() ; forms.attach(interactive)
_ = Page(name="default", title=u"Application Forms", description=u"", content=u"""h1. Welcome to Application Forms""") ; _.save() ; _.attach(forms)

_ = Page(name="council", title=u"Council", description=u"", content=u"""h1. Mayor and Council

*The Town of Comox is governed by a Mayor and six Councillors, elected at large for a term of 3 years. The current term runs from December 1, 2008 until November 30, 2011.*

h2. COMOX STRATEGIC PLAN 2010-2014

Click here for Council's Strategic Plan 2010-2014.

h2. COUNCIL MEETINGS:

*Regular Council Meetings* are scheduled for the first and third Wednesday of each month at 5:30 pm and;

*Committee of the Whole Meetings* are scheduled for the second and fourth Wednesday of each month at 4:15 pm.

Click here for "2010 Council Meeting Dates":/hall/meetings/cm-dates .

All meetings are held in *Council Chambers* located at: 1801 B Beaufort Avenue, (beside d'Esterre Senior Centre). 

If you would like to appear before Council, click here for the "Request to Appear as a Delegation":/interactive/forms form.

Read "Agendas and Minutes":/hall/meetings on this site. 

 


h2. MAYOR AND COUNCIL MEMBERS

The Mayor is Paul Ives and the Councillors are:
Russ Arnott, Patti Fletcher, Ken Grant, Tom Grant, Marcia Turner.

Appointments to Boards and Committees: Council Committee List (2009-2010)

Read Paul Ives "Inauguration Speech.":/discover/mayor

 

h2. CONTACT INFORMATION:

If you would like to send a message to Council as a whole, please send to council@comox.ca and each member will receive a copy of your message. Please include your full name and address with your message.

 

h3. MAYOR PAUL IVES

Home Phone: 250-339-9109

Business (Town Hall) FAX: 250-339-7110

Email: pives@comox.ca

 

h3. COUNCILLOR RUSS ARNOTT

Home Phone: 250-339-2569

Business (Town Hall) FAX: 250-339-7110

Email: rarnott@comox.ca

  

h3. COUNCILLOR PATTI FLETCHER

Home Phone: 250-339-6766 / Work Phone: 250-339-6683

Business (Town Hall) FAX: 250-339-7110

Email: pfletcher@comox.ca

 

h3. COUNCILLOR KEN GRANT

Home Phone: 250-339-1355

Business (Town Hall) FAX: 250-339-7110

Email: kgrant@comox.ca

 

h3. COUNCILLOR TOM GRANT

Home Phone: 250-339-7761

Business (Town Hall) FAX: 250-339-7110

Email: tgrant@comox.ca

 

h3. COUNCILLOR MARCIA TURNER

Home Phone: 250-339-0167

Business (Town Hall) FAX: 250-339-7110

Email: mturner@comox.ca""") ; _.save() ; _.attach(hall)

_ = Page(name="financial-plan", title=u"2010 Financial Plan", description=u"", content=u"""h1. 2010 Financial Plan

*Council adopted its 2010 - 2014 Five-year Financial Plan Bylaw on May 12th. The summary below highlights decisions made through the process of drafting that plan. There are links to related documents at the bottom of this page.*

<hr>

h4. May 5th and May 12th Council Meetings

On May 5th Council gave three readings to the Financial Plan Bylaw, with the changes that had been recommended at the April 28th Committee of the Whole meeting, along with a Tax Rates bylaw. A week later on May 12th, Council adopted those bylaws.

 

h4. April 28th Committee of the Whole

Staff presented the revised draft of the full Financial Plan along with draft Financial Plan (2010 – 2014) and 2010 Tax Rate Bylaws for the Committee to review and discuss.  The proposed Town General Tax increase for 2010 is 3.7% for residential taxpayers and 3.2% for business assessment. When combined with this year’s freeze on utility fees and parcel taxes, the net effect of the Financial Plan on an average single family home will be an increase of $27.61. The Committee recommended making two changes to the Plan – shifting $176,100 that was budgeted for debt repayment to a capital reserve for affordable housing initiatives, and reducing the contribution from the water fund to a water meter replacement reserve in 2012 – 2014 (limiting the contribution in those years to the $25,000 budgeted in 2011). Then the Committee recommended that the bylaws be forwarded to Council (scheduled to meet May 5th) for three readings.

 

h4. April 14th Committee of the Whole

Staff presented the first draft of the full Financial Plan (revenue, department expenditures and capital expenditures) for 2010 through 2014 for the Committee to review and discuss.  Based on a 2010 tax increase of just under 4%, the Committee reviewed these budgets and recommended a number of changes to reduce net expenditures. These changes included a $10,000 reduction to 2010 Council travel and conference, $2,000 reduction to 2010 Mayor’s travel and conference, $5,000 from 2010 bylaw enforcement (for misc expenditures), and a $2,500 increase to the grants to the Sid Williams Theatre from the Town for 2010. Council will have to ratify these changes, then a final draft financial plan (including bylaw) will be submitted to the Committee April 28th. Council must adopt the Financial Plan bylaw (and a Tax Rates bylaw) by May 14th. 

 

h4. March 10th Committee of the Whole

Staff presented the first draft of the Public Protection (Police, Fire Department, Building Inspection) and Planning budgets for 2010 through 2014 for the Committee to review and discuss.  These budgets show projected expenditures for these services.  The cover memo explains that this first draft was prepared on the same basis as prior years with no significant changes to operations proposed for any of these departments. The Planning budget has significant project expenditures (for review of the Official Community Plan, and development of a comprehensive pedestrian and traffic safety study in 2010) that have an increased for 2010. 

 

h4. February 24th Committee of the Whole

Staff presented the first draft of municipal utility (garbage, water, and sewer) service's budgets for 2010 through 2014 for the Committee to review and discuss.  These budgets show both revenue and expenditures (operating and capital) for these services, along with the net surplus or shortfall in projected net revenue for the next five years.  The cover memo explains that this first draft was prepared on the basis of no overall rate increases in 2010 or subsequent years, but due to a net shorfall of revenue in the water fund, this will be harder to maintain there than in the garbage and sewer services.  The memo says that Council might want to consider transfering $15 from the sewer parcel tax to the water parcel tax starting in 2011 to help deal with this.  Holding fees steady for all three services is dependent upon resource utilization remaining steady (or declining in the case of the water service) and no significant increases to fees charged by the Regional District for operation of the landfill, supply of water and treatment of sewage. 

 

h4. February 10th Committee of the Whole

Staff presented two reports to the Committee to start its work on the upcoming Financial Plan in earnest.  The first memo explained the requirement (of the Community Charter) that we include Revenue Objectives & Policies as part of our annual five-year Financial Plan.  The memo went on to review the Objectives & Policies adopted in the last Plan.  Arising from discussion, the Committee passed a motion to delete Section 2 of Revenue Policies.  In 2009 this Section said that there would be a 4% general tax increases to all classes of property from 2009 to 2013.  If Council adopts the Committee's recommendation, this would free up Council to have different general tax increases in different years, and to vary the increases by property class.

Next, the Committee was provided with worksheets updating the balance of, and committments made to date from the Town's Federal Gas Taxes (Community Works) Funds.  These come to Canadian municipalities from the Federal Government, and must be spent on "green" capital expenditures and on capacity building studies.  The Committee passed a motion to increase the funding allocation for energy efficiency upgrades of Town buildings to $250,000 including a lighting upgrade to the firehall and a study of geothermal heating at the Recreation Centre this year.

Finally, the Committee was presented with a first draft of a Capital Plan for 2010 to 2014.  Capital expenditures form roughly 25% of our total expenditures, so they have a significant effect on the revenue needed over the next five years.  The Committee passed a motion to advance the budget for constructing a (yet to be selected or designed) bike lanes from 2013 in the Financial Plan to 2011.

 

h4. February 3rd Regular Council Meeting

Council received and adopted its Strategic Plan for 2010 to 2014.  This is a high level document that lays out Council's three strategic priorities over the next five years: 

* *Sustainable Infrastructure* (related goals:  improving road & sidewalk condition, maintaining utilities infrastructure, and assessing future infrastructure needs)
* *Sustainability and Livability* (related goals:  increase environmental responsibility, increase recreational opportunities, increase long-range planning activities, become a more inclusive community, increase local economic development opportunities, and increase health services)
* *Good Governance* (related goals: improve/maintain high level of customer service, impvoe communication with public, enable and motivate staff, and support regional initiatives).
These Strategies and Goals will be reflected in the upcoming Financial Plan.

 

h4. January 27th Committee of the Whole

Staff presented two reports to Council's Committee of the Whole (so called because all Council members sit on this Committee).  The first was a report on the initial (Completed) Assessment Roll for 2010.  The next was a report reviewing the 2009 - 2013 Financial Plan (adopted last year).  At its next meeting (February 10th) the Committee will discuss its Revenue Objectives & Policies that determine what rate increases will be built into its new Financial Plan.  Both of the staff reports at this meeting are now listed on the related items (items 01 & 02 below).  They were received and discussed by the Committee, but no motions arose from the discussion.  Had any motions related to the Financial Plan been adopted by the Committee, they would be subject to ratification at a Regular Council Meeting.

 

h4. Background

Municipalities in BC are governed by the Community Charter, which requires them to adopt annually by bylaw, five-year Financial Plans.  This must be done before a property tax bylaw is adopted.  The deadline for both is May 14th of each year.  Until adoption of a new Financial Plan bylaw, the bylaw from the previous year provides the legal authority for expenditures.

 

h4. Related Documents on our website:

2010 Financial Plan Bylaw
Proposed Taxes & Fees on Average Single Family Home (2010)
Proposed 2010 Comox Property Tax Rates 
Draft Tax Rates Bylaw
Revised Draft Financial Plan Detail
Staff Memo on Revisions to Draft Financial Plan
First Draft of Full Financial Plan
First Draft of Full Financial Plan
First Draft of Public Protection and Planning Budgets
First Draft of Utility Budgets
First Draft of Capital Plan
Schedules on Federal Gas Tax Funds
Report on Revenue Objectives & Policies
Council's Strategic Plan 2010 to 2014
Report on Completed 2010 Tax Roll
Review of 2009 to 2013 Financial Plan
Financial Plan 2009 to 2013 Detail""") ; _.save() ; _.attach(root)

water = Folder(name="water", title=u"Water Documentation", description=u"", default="view:details") ; water.save() ; water.attach(root)
_ = Page(name="meter", title=u"Water Metering Program", description=u"", content=u"""h1. Meter Program Information

*Explanation of the Town's 2010 Meter Program, with application attached:*
h2. Background to the water metering program
 
Comox buys its water from a Regional District water system that provides Courtenay, Comox and certain rural service areas with their water.  Last year the Town spent $1.4 Million buying 2.6 billion litres of water.  This Regional District water system has a licenced annual limit on the water that it can draw of just over 9 billion litres per year.  In order to comply with its licence over the long-term despite a growing population of users, the Regional District has adopted a water efficiency plan that proposes a 27% reduction in water use through a broad series of initiatives including water metering, public education, low flow toilet rebates, faucet & showerhead replacements, rain barrels, leak detection and repairs, water use restrictions and enforcement.  Of all these activities, water meters are predicted to provide most of the water use reductions.

The Town will participate in these programs in order to help the Regional District’s water system reach its targets.  We are helping to distribute the information on toilet and rain barrel rebates.  We already repair any water leaks reported, and we will work with the Regional District to detect previously unknown leaks, which we will then fix.  We have already been replacing water appliances (toilets & faucets) in Town buildings with more efficient ones.  That process will continue in 2010.  We will be working with the public on water education and will build a demonstration low watering (xeriscaping) boulevard (site still remains to be determined).  And we will continue to investigate complaints received about violations of sprinkling regulations, as we have in prior years.

With regard to water meters, Council has decided to implement a residential metering project in 2010 that would meter residential strata customers, meter ready homes, and other customers who ask for meters to be installed.  *Council also decided that the customers who get a meter will be allowed to keep paying flat-rate user fees unless they volunteer to be billed by their metered water use.*

The cost of this metering program ($1,350,000) is funded $471,000 from the Regional District, $450,000 from Federal Gas Taxes, $250,000 from our Water Fund Capital Reserves, and $179,000 from 2010 Water Fund User Fees.  No debt will be needed to pay for these meters nor did we have to raise water user fees this year to pay for this project.

We expect that this project could meter up to 40% of our residential customers since there are strata developments including over 1,000 residential units in Comox and over 900 meter ready homes

Installation of meters will begin this summer.  Then we will begin reading the meters, and share the data back with the owners of the metered residences.  The soonest they would be able to switch (*if they want*) to metered billing would be for 2011 (2010 fees will already have been billed with property taxes and paid by July 2nd).

We currently charge residential water customers $303 per year for their water use.  Metered businesses are charged $0.78 / m3 for metered use of water.  We have only gathered a limited amount of data on residential water use in Comox, because less than 200 Comox homes have water meters.  But the data we do have (from the homes with meters) shows that many homeowners use less water than average, so they could reduce what they are paying for water by volunteering to be billed by their meter.  The choice will rest with individual property owners and the strata councils, once they know from their own meter readings what their consumption patterns are.

 

h3. Questions we’ve been asked about this program so far

Q: *Who can ask for a meter to be installed?*

Any residential property owner who is not in a strata unit or a meter ready home (since those homes will get a meter already).

Q: *How do I know whether my home is meter ready or not?*

If you have a meter box then your home is meter ready.  Since 2001 subdivisions in Comox have included a meter box installed for each water connection.  As well, there have been other homes made meter ready if we were repairing their water services.  Those have meter boxes on their connections too. 

Q: *How much will the Town charge to install a meter?*

We are not charging home owners or residential strata to install their meters.  That being said, this program is partially funded out of our water system, which we all pay into.

 

Q: *What if I don’t want the Town to install a meter in my meter box?*

Sorry, but if your house has a meter box already, we will be installing a meter under this program.  The Town has the right to do that under its Water Regulations & Rates Bylaw adopted in 1979.  The key is that Council’s motion allows you to continue to pay flat water rates unless you volunteer to be billed by your meter.

Q: *How often will the meters be read?*

The meters will be read electronically so we can read them as often as required.  This will likely be monthly – particularly as we expand our data gathering on residential water use and try to reconcile it to our monthly water purchases.

Q: *How often will the Town bill residential metered customers?*

That has yet to be finalized, but the likely answer is either two or four times per year.  We are implementing new billing software, but there is still a cost associated with billing customers and we will want to be as efficient as we can.

Q: *What if my meter shows that there is a water leak on my water connection?*

The meter is installed at the connection point between the Town’s system and your property.  If there is a water leak beyond the meter, it is on your property and it is your responsibility to call a plumber to fix it. 

Q: *What if there is a leak on private property and the owner will not fix it?*

Our current water fees bylaw allows us to charge metered residences that use an excessive amount of water (which we define as average water use over time of 52 or more m3 of water per month).  If a property has a leak and the owner will not fix it, then we will bill the owner for this use.  We chose 52 cubic metres (52,000 litres) of average water use per month as the amount of residential water use that we consider excessive because it is more than twice the amount of water that we think most homes use (on average) through a year.

Q: *If I volunteer to be billed by the meter and then increase my water use in the future, can I go back to flat-rate billing?

No – the purpose of installing meters is in part to encourage people to reduce their water use over the long term. 

Q: *If meters are installed this year, is 2011 my only opportunity to volunteer for metered billing?*

No – we will continue reporting water use to owners even if they don’t switch in 2011.  Then, if they want to switch in 2012, or later years, they can still do that.  However, because we bill flat-rate residential water fees on tax notices, owners will have to switch at the start of a year.

Q: *If I get a meter and then don’t volunteer to be billed by its readings, how long can I keep paying flat rates?*

Council’s motion was open-ended.  There was no deadline for switching.

Q: *How much could I save with a meter?*

The only way you will know for sure is if you ask for a meter to be installed and then see how much water you use.  After that, you can calculate whether or not you could save anything and decide whether or not to change to metered billing.

Q: *Why did the Town pick meter ready homes and residential strata for this project?*

We can meter more of these customers for less cost than single family homes that are not meter ready (because of landscaping restoration costs). 

Q: *Is there a limit to how many residences could ask for a meter this year?*

Yes.  Most of our budget for the project is allocated to the meter ready homes and residential strata.  What budget is left will probably fund 100 to 200 additional homes volunteering for meters.  So, if you want to be included, we encourage you to contact us as soon as possible and get on our list of installations. 

Q: *What is involved with installing a meter?*

If a property is meter ready then we lift the lid on the meter box, turn off the service for a few minutes, and install the meter.  There is minimal cost and disruption of service.  No digging is required, assuming that the meter box hasn’t been disturbed since it was installed.

For homes without meter boxes, we have to dig up the water service at the edge of the property and install several pieces of hardware including a meter setter (goose-necked pieces of pipe that have a shutoff valve on one side and a backflow preventer on the other, with a space for the meter in between), a meter box, the meter and a small transmitter with a battery.  Then we restore the landscaping (lawn, plants, or sometimes even a driveway) where we dug up the service, to return the property (as best we can) to its original state.

Q: *Wouldn’t it be simpler to install a meter in the house?*

While for many homes that might be true, there are a number of problems with that, including getting future access to the meter in case we need to maintain or replace it.  Also, because irrigation systems usually tie into the service line going to the house, an inside meter would miss the water used by most irrigation systems. 

Q: *How do I get a meter installed?*

Print & complete this Application to Install a Residential Water Meter form then provide it to Comox Town Hall by either: mail, deliver, fax or email - contact information is on the form and appears as follows:

h3. Application Form

To print only the application, highlight the lines below then print your section.

 

 Town of Comox  
1809 Beaufort Avenue     Comox, B.C.    V9M 3L6
fax:  250-339-7110   email:   town @ comox.ca

Application to Install a Residential Water Meter
 

_______________________________              _________________________   

            Owner Name(s)                                Residential Address

 

_______________________________              ________________

            Email address (optional)                     Daytime Phone #

I/we are owners of the above property, and hereby request that the Town of Comox install a residential water meter on this home, in accordance with Council’s December 2, 2009 motion that residential customers who are metered be allowed to keep paying flat-rate user fees unless they volunteer to be billed by their metered water use.

I/we understand that I/we will have the opportunity to volunteer for being billed by our metered use only after the Town has measured our water use and reported it to me/us.

I/we also understand that it is the property owner who is responsible for repairing water leaks on their property if the meter identifies there is one.

 

_______________________________________________              __________________

Owner Signature(s)                                                                 Date Signed""") ; _.save() ; _.attach(water)

