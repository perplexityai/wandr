Solve the following task and write the results to the specified JSONL file.

## Universal rules

The following rules apply to every task below.

**Identifier discipline.** Same entity → same string. Different entities → different strings. When you're unsure whether two names refer to the same thing (spelling variants, model editions, product versions), don't offload the ambiguity to the user — decide and commit. Don't hedge by splitting "just in case" or merging "probably close enough." Both failures cost credit.

**More is (usually) better.** Whenever the task says "at least N" / "N+" / etc, going past N generally helps your score — treat those as soft floors, not exact targets.

**No duplicate entities.** Do not, however increase volume via duplicate entities, all the entities must be meaningfully different, entity-duplicating rows will generally be penalized; in particular, do not supply multiple rows per entity to "supply the answer in chunks", which will also be treated as entity duplication.

**Every `url` you submit must be fetchable.** Do not submit URLs you expect to be non-resolvable (DNS failure, dead host) as your `url`. Evidence should come from an available `url` (even if you wished to, say, provide evidence for some URL's unhealthiness).

**Every row carries `excerpts`** — verbatim or near-verbatim quotes from the source page (whitespace, punctuation, ellipses to skip irrelevant clauses are fine) **with semantics preserved**. An excerpt is what the page literally says, in the meaning the page intends. Fabrication, paraphrase that shifts meaning, sentence-stitching across sections, or selective cropping that flips a hedge into confidence — all fail.

The excerpts collectively make the answer evident. *Every* task-required claim / task-asked question / answer field / etc MUST have its support visible somewhere in the excerpt set — not just nearby on the page. The reader's test: imagine someone sees only your excerpts (with no access to the rest of the page); can they verify each piece of your answer? If a page genuinely doesn't carry what the task asks for, find a different page or skip the entity rather than fish for tangential excerpts. If you deem paraphrasing necessary / desirable for proper answer delivery, that's admirable and encouraged: paraphrase to your heart's desire within `answer` fields, make new `answer` fields and redistribute summaries among them as you see fit, but excerpts stay faithful and fully evidence-complete.

**Page contents only.** This is a task about citing web pages for human consumers, and citations are expected to be human-usable — both in where they are sourced from and in how well they stand on their own, out of page context. Excerpts come from the web-page main text — what a human reader sees on the page. Excerpts should also look sensible by themselves, with their information-bearing intent clear. API response blobs, page metadata fields (timestamps, view counts, score numbers), structured-data payloads (`__NEXT_DATA__`, JSON-LD, OpenGraph), and other “robot-side” sources / page representations are out of scope. In a similar vein, be wary of citing image captions / on-hover alt text / infoboxes / specially rendered bibliography or reference units / UI or navigation elements / etc. (unless confident in both their visibility and critical utility for the task), and avoid citing image contents, hyperlink-encoded URLs, and similar evidence surfaces altogether: anything outside the straightforward “main body of text” risks reducing citation ergonomics to the point where it is considered unusable.

**Signaling absence.** If you mean for a blank or sentinel `answer` field to assert "this required information isn't on the page" (vs. "I missed it"): first verify the task warrants such an option — many tasks treat blank-required as an invalid entity. When absence IS admitted, flag the intent explicitly in an appropriately-named `answer` field, and let your excerpts carry the strongest available evidence — direct proof-of-absence ("not listed", "n/a") if the page provides it; otherwise, try at least capturing the page segments where the missing info would plausibly have appeared if it existed, where applicable.

## `forbes_250_errors`

For at least 40+ *verifiable* factual errors across the 250 biographies in the Forbes "Self-Made 250: The Greatest Living Self-Made Americans" article below, identify each error as a *verbatim* restatement of the Forbes text (not enriched / paraphrased / derived whatsoever: source-side details — the actual fact, the contradiction's mechanism, derived computations like recomputed ages — belong in corroborating-source citations, not in the error-statement text, which is used for in-article identification) and supply a *credible* source (i.e. 1+ URL — official records, major newspaper, encyclopedia, etc.) per claim that contradicts the Forbes statement.

Date-relative claims (notably bio ages, time-since-event statements) are evaluated against the article's publication date (April 14, 2026, visible in the article header below), not today's date. A bio listing "X, 82" is correct if X had turned 82 by April 14, 2026; subsequent birthdays don't retroactively make the bio wrong.

The article text is provided below.

#### Published April 14, 2026

#### Edited By Alex Knapp and Luisa Kroll , Forbes Staff

#### Reported By Jessica Jacolbe and Chase Peterson-Withorn

**Grit. Hustle. Resilience. ** The American Dream is built on the audacious belief that anyone can make it to the top. Every elementary school kid is imbued with the belief that anyone can become president of the United States. Or a hip-hop megastar. Or a space-faring billionaire. The notion is as old as the Republic and stands self-consciously in contrast to class-ridden Europe where one’s prospects were often determined at birth.

This ideal has always had its heroes: from Alexander Hamilton, the orphaned immigrant who crafted America’s first financial system, to Andrew Carnegie, who went from working as a young teen in a textile mill to forging a vast steel empire. Since 1917, it has been the prime subject matter of this publication. So, in honor of America’s semiquincentennial, we feel uniquely qualified to rank the 250 greatest living self-made Americans. (Our list of the 250 greatest historic self-made Americans can be found here).

To identify these revolutionaries, we first mined *Forbes*’ 109-year-deep archive for classic tales of entrepreneurial capitalism. Then we asked our current crop of beat reporters for their ideas. We canvassed AI, running hundreds of queries through both ChatGPT and Gemini. While we put a heavy emphasis on rags-to-riches billionaires, we also included pioneering scientists, Supreme Court justices and others whose “wealth” is measured in influence and impact, not just dollar signs.

Next, we ran names past a panel of expert judges: **DeAngela Burns-Wallace**, CEO of the Kauffman Foundation; **Keith Dunleavy**, Founder, Inovalon; **Rich Karlgaard**, Former Publisher, *Forbes*; **Steven Klinsky**, Founder and CEO, New Mountain Capital; **Jim McKelvey**, cofounder of Block (formerly Square); and **Ryan Rippel**, CEO of NextLadder Ventures.

An invaluable resource was *Forbes*’ Self-Made Score, a 1-to-10 ranking that quantifies the “distance traveled” by each individual—separating those who started with nothing from those with a big head start. Only those ranking nine or ten made the cut. The final ranking encompasses financial success, obstacles overcome and enduring impact.

## FORBES 250

## The Greatest Self-Made Americans

## #1-50

#### ★ = BILLIONAIRE

#### #1. Oprah Winfrey , 72 ★

#### Born to a teen mother, Winfrey grew up on a rural Mississippi farm without indoor plumbing. At 9 she was raped by a cousin; at 14 she gave birth to a son, who died soon thereafter. Thanks to a federal program, she attended a rich suburban school where she discovered a knack for public speaking and debate, which earned her a part-time radio gig and, later, a scholarship to Tennessee State University. In 1984 she took over a struggling morning talk show in Chicago and eventually turned it into a national media brand.

#### #2. Harold Hamm , 80 ★

#### The 13th child of Oklahoma sharecroppers, Hamm’s earliest memory is picking tomatoes with his bare feet in the red Oklahoma dirt. He eventually started his own trucking company hauling water to and from oilfields, then in 1971 took out a loan to drill his first well. The fracking pioneer helped turn the U.S. into the world’s biggest oil producer.

#### #3. David Steward , 74 ★

#### His father worked as a mechanic, janitor and trash collector to support eight children. Growing up in segregated Missouri, Steward was part of a group that pushed his town to integrate its swimming pools as a teenager. He walked on to his high school basketball team and earned a college scholarship. Even after he first cofounded World Wide Technology, now one of the largest IT services companies on the planet, he sometimes went without a paycheck and once watched his car get repossessed.

#### #4. Thomas Peterffy , 81 ★

#### In 1965, a 21-year-old Peterffy arrived at John F. Kennedy airport nearly penniless after fleeing Communist Hungary, hoping to live with his father. Turned away with $100, he got a job as a programmer and eventually saved enough to buy a seat on the American Stock Exchange. He went on to pioneer automated digital trading with his firm Interactive Brokers.

#### #5. LeBron James , 41 ★

#### His teen mom struggled to find steady work or a stable home, leading to him moving a dozen times in three years. At 9, the fatherless Akron, Ohio native moved in with the family of a local football coach, who introduced him to basketball. Drafted to the pros in 2003 right out of high school, he became the first active NBA player to become a billionaire.

#### #6. Jan Koum , 50 ★

#### After immigrating at age 16 from Ukraine to Mountain View, California, Koum and his mom moved into a small two-bedroom with government assistance. He signed the deal to sell WhatsApp, which he cofounded, to Meta at the same building where he once stood in line to collect food stamps.

#### #7. Dolly Parton , 80

#### The country singer grew up “dirt poor” with her 11 siblings in a Tennessee shack without running water or electricity. She moved to Nashville after high school, using her songwriting talent to pen top 10 hits for the likes of Kitty Wells and Hank Williams Jr. before becoming a star in her own right.

#### #8. Bill Clinton , 79

#### Clinton, whose father died before he was born, was determined to become president of the United States from an early age, despite growing up in a household afflicted by poverty and domestic abuse. He later got a scholarship to Georgetown University, won a prestigious Rhodes Scholarship and attended Yale Law School. He became a law professor before being elected Arkansas attorney general, then governor, then the 42nd president.

#### #9. Diane Hendricks , 79 ★

#### Hendricks became a teen mother at age 17, forcing her to drop out of school. She later worked as a Playboy Bunny to support her child before meeting her second husband, Ken. The pair cofounded ABC Supply, one of the world’s largest construction supply firms, and ran it together until 2007, when he died after falling through a roof where he was checking construction.

#### #10. J.D. Vance , 41

#### Raised in Ohio’s Rust Belt, Vance faced financial struggles and family instability due to his absent father and his mother’s drug addiction. Raised by his grandmother, who owned 19 handguns and provided tough love, he served in the Iraq War as a Marine, then earned a law degree from Yale and became a venture capitalist. His memoir, Hillbilly Elegy , garnered national attention, and he was elected to the Senate in 2022 and became vice president of the U.S. in 2025.

#### #11. Larry Ellison , 81 ★

#### Ellison’s unmarried, 19-year-old mom gave him up for adoption at nine months after he contracted pneumonia. He was raised by his great aunt and uncle, who lost his real estate business in the Great Depression and made a modest living as an auditor for the public housing authority. He later dropped out of college twice before becoming a tech titan.

#### #12. George Soros , 95 ★

#### He survived Hungary’s Nazi occupation as a child and put himself through the London School of Economics working as a railway porter and waiter on his way to becoming one of the world’s most influential financiers.

#### #13. Donald Friese , 85 ★

#### Orphaned as a child, Friese worked on a dairy farm at age 12 before enlisting in the Army. After a three-year tour of duty, he moved to California with $125 and landed a job at the warehouse of C.R. Laurence, which he eventually took over and then sold for $1.3 billion in cash in 2015.

#### #14. David Walentas , 87 ★

#### As child farmworkers, he and his brother were “something between an orphan and an indentured servant.” (see “Six Lessons From A Billionaire Who Once Sold His Blood To Buy Food”)

#### #15. Howard Schultz , 72 ★

#### Schultz grew up in a Brooklyn housing project. When he was 7, his dad, a cloth diaper delivery driver, fell on the job; he had no insurance or salary. The first person in his family to graduate from college, Schultz attended Northern Michigan University on a football scholarship. He joined a small company called Starbucks in the 1980s; the rest is history.

#### #16. Clarence Thomas , 77

#### His father deserted his family when he was very young. His mother sent Thomas, age 7 at the time, and his younger brother, Myers, to live with their maternal grandparents in Savannah, providing more stability but no indoor plumbing. Educated at a segregated Catholic school, he went on to Yale Law School and, in 1991, the Supreme Court of the United States.

#### #17. Bob Parsons , 75 ★

#### The child of hardcore gamblers, Parsons grew up “poor as a church mouse” in inner-city Baltimore. School was no refuge as he failed 5th grade and almost flunked 12th. Enlisting in the Marines, he was sent to Vietnam in 1969. He came back with PTSD but with focus. He taught himself to code and started several businesses, including web hosting firm GoDaddy.com, which he eventually sold to investors including KKR.

#### #18. Jay-Z , 56 ★

#### Raised in Brooklyn’s notorious Marcy housing projects, Jay-Z was a drug dealer before becoming a musician. He cofounded his own music label when nobody would give him a record deal for his debut album.

#### #19. Sonia Sotomayor , 71

#### Sotomayor grew up in a Bronx housing project. She was diagnosed with juvenile diabetes at age 7. Her father died when she was 9. After attending Catholic schools, she made it to Princeton, where she easily qualified for financial aid given that her family didn’t have a bank account. She became a Supreme Court Justice in 2009.

#### #20. Dr. Dre , 61 ★

#### The rapper cut grass to buy shoes when he was a kid. “I would do what I had to do.” (see “ Dr. Dre On Becoming A Billionaire ”)

#### #21. Shahid Khan , 75 ★

#### The Pakistani immigrant arrived with $500 in his pocket and worked nights as a dishwasher while studying at the University of Illinois at Urbana-Champaign. He later designed a one-piece truck bumper, the basis of his $15 billion fortune.

#### #22. Dennis Washington , 91 ★

#### Montana’s wealthiest citizen survived childhood polio, lived in government housing during World War II and shined shoes as a kid to make pocket money.

#### #23. Magic Johnson , 66 ★

#### The NBA star was raised in a working-class family with nine siblings in a three-bedroom apartment. He retired from the NBA in 1991 after being diagnosed with HIV. Nearly all of his fortune comes from post-basketball business ventures.

#### #24. John Paul DeJoria , 81 ★

#### The cofounder of hair care company John Paul Mitchell Systems and high-end tequila Patrón Spirits Company, DeJoria spent time in foster care and twice was homeless, living out of his car.

#### #25. Tyler Perry , 56 ★

#### The once-homeless, “poor as hell” producer and director dealt with more than just poverty growing up in New Orleans; he describes an upbringing by an abusive man he later learned was not his father. Inspired to write out his stress, he dropped out of high school and started performing the plays he wrote in small theaters.

#### #26. Ralph Lauren , 86 ★

#### Before he was a fashion mogul, Lauren shared a two-bedroom Bronx apartment with his immigrant parents and three siblings.

#### #27. Noubar Afeyan , 63 ★

#### With his family, the healthcare entrepreneur and venture capitalist fled Lebanon in the 1970s; they rebuilt in Montreal from scratch.

#### #28. Herbert Wertheim , 86 ★

#### The child runaway faced truancy charges at age 16 but was given the choice between reformatory school or the Navy. He joined the latter on his way to becoming a successful optometrist-inventor-investor.

#### #29. Henry Samueli , 71 ★

#### The son of Polish Holocaust survivors who moved to America with next to nothing, Samueli spent his childhood helping at his parents’ modest liquor store before falling in love with engineering and cofounding semiconductor giant Broadcom.

#### #30. Harry Stine , 84 ★

#### The soybean billionaire grew up on a farm and struggled with dyslexia before unlocking his talent for genetics.

#### #31. Daniel D'Aniello , 79 ★

#### The Carlyle Group cofounder started bagging groceries as a child to help his single mother, who worked four jobs, make ends meet.

#### #32. Dick Portillo , 86 ★

#### The hot dog tycoon grew up in public housing.

#### #33. David Geffen , 83 ★

#### The Hollywood titan was born to working-class immigrant parents and started in the mailroom of the William Morris Agency.

#### #34. Yvon Chouinard , 87

#### Chouinard hails from a working-class background and spent much of his 20s rock climbing, living out of his car on 50 cents a day and even eating squirrels before founding Patagonia, which he famously gave away to fight climate change.

#### #35. Igor Olenicoff , 83 ★

#### The real-estate kingpin’s family fled the Soviet Union for Iran, where Olenicoff was born, and arrived in the U.S. with $800.

#### #36. Eric Smidt , 66 ★

#### Smidt spent four years in an orphanage before building mail-order powerhouse Harbor Freight Tools.

#### #37. Arthur Blank , 83 ★

#### Born in Sunnyside, Queens, he lived in a single-bedroom apartment. His father died when he was a teenager, and Blank did landscaping and ran a laundry service to pay for college. He was later fired from a hardware store before cofounding Home Depot.

#### #38. Neil Bluhm , 88 ★

#### Bluhm’s father left when he was 13, and he worked through law school before building a real-estate empire.

#### #39. Joe Kiani , 61 ★

#### Kiani’s family lived in a housing project after fleeing Iran; on his own by 14, he funded his education.

#### #40. Fernando De Leon , 47 ★

#### The real estate titan, whose dad died when he was 12, crossed the border from his meager home in Mexico daily to attend school in Texas. “My psyche was always a poor man’s psyche,” he says.

#### #41. Hayes Barnard , 54 ★

#### The fintech billionaire was raised by a single mother (his alcoholic father left when Hayes was 3) and overcame dyslexia to start home upgrade financing firm GoodLeap.

#### #42. Michael Polsky , 77 ★

#### The energy kingpin and his pregnant wife immigrated from Ukraine in 1976 with $500 and four suitcases. The charity that helped them resettle suggested a blue-collar job, but instead he sent out hundreds of résumés before getting an engineering gig at a power plant.

#### #43. Frank VanderSloot , 77 ★

#### The Melaleuca founder labored on the family farm while his father worked the railroad; he lived in a laundromat during college.

#### #44. Ken Langone , 90 ★

#### The son of a plumber and cafeteria worker, Home Depot’s investment banker dug ditches for the Long Island Expressway before getting his degree in economics.

#### #45. David Hoffmann , 73 ★

#### His home had no hot water until he hit high school. (see “This Billionaire Wants To Save America’s Newspapers. He Thinks He’s Found A Way”)

#### #46. Haim Saban , 81 ★

#### The Egyptian refugee lived in a one-room Tel Aviv apartment before immigrating to the United States and becoming a media mogul.

#### #47. Jay Chaudhry , 66 ★

#### The tech billionaire’s home in a village in India had no electricity or running water.

#### #48. Omar M. Yaghi , 61

#### The child of Palestinian refugees, the Nobel Prize winner moved to the U.S. at age 15 to attend college.

#### #49. Israel Englander , 77 ★

#### The son of Holocaust survivors, the hedge fund billionaire grew up in Brooklyn and started trading stocks in high school.

#### #50. Arnold Schwarzenegger , 78 ★

#### Born into a poor family in a small town in Austria, Schwarzenegger used his bodybuilding and extra cash from laying bricks and selling fitness pamphlets to buy apartment buildings even before becoming a movie star.

## #51-100

#51-100

#### ★ = BILLIONAIRE

#### #51. Roy Carroll II , 63 ★

#### The construction tycoon mowed lawns, returned bottles and sold candy to save up for his first house, which he bought at age 14.

#### #52. Whoopi Goldberg , 70

#### The EGOT (Emmy, Grammy, Oscar and Tony) winner faced periods of homelessness early on and worked odd jobs like mortuary cosmetologist.

#### #53. Hemant Taneja , 51 ★

#### The venture capitalist immigrated from India at 15 and worked full-time during high school to help support his family.

#### #54. Mario Capecchi , 88

#### While his mother was incarcerated in Germany, possibly at Dachau, during World War II, the Nobel winner spent his childhood on Italy’s streets.

#### #55. Isaac Perlmutter , 83 ★

#### The billionaire behind Marvel’s huge success immigrated to the U.S. from Israel with just $250 in 1967 and sold toys on Brooklyn streets.

#### #56. Mark Stevens , 66 ★

#### The venture capitalist and Nvidia board member partially funded his college education as a fast-food cook.

#### #57. John Menard Jr. , 86 ★

#### The founder of retail giant Menards grew up in rural Wisconsin after his dad gave up teaching for dairy farming.

#### #58. David Sun , 74 ★

#### The cofounder of Kingston Technology was raised by a single mother in Taiwan.

#### #59. Douglas Leone , 68 ★

#### The venture capitalist came from Italy at age 11 and recounts being bullied in school before working his way through college.

#### #60. Bruce Springsteen , 76 ★

#### The Boss grew up in a working-class New Jersey town and played clubs and bars before becoming a star.

#### #61. Viola Davis , 60

#### The EGOT winner grew up in “abject poverty” living in rat-infested, condemned buildings and eating out of garbage cans.

#### #62. John Tu , 84 ★

#### Tu’s family fled from China to Taiwan. He went to school in Germany, where he worked as a cook. He couldn’t get an engineering job in the U.S., so he opened up a gift shop that failed before cofounding Kingston Technology.

#### #63. Gail Miller , 82 ★

#### Raised in a house with one light bulb that was moved from room to room, the billionaire and her husband risked their savings to buy their first business, a Toyota dealership.

#### #64. Brandi Carlile , 44

#### Financial instability caused the Grammy winner’s family to move 14 times in 14 years and she busked her way to music stardom.

#### #65. Barbra Streisand , 83

#### The EGOT winner was raised by a single mother in a Brooklyn tenement after her father passed away.

#### #66. Tilman Fertitta , 68 ★

#### Fertitta, who learned the food business at his father’s seafood restaurant, dropped out of college to pursue business ventures, obtaining a loan at age 23 that he used to build his first hotel. He later got into restaurants with Landry’s seafood.

#### #67. Chris Gardner , 72

#### Born into poverty, Gardner was a homeless single father before becoming a stockbroker and founding his own firm.

#### #68. Jeff Greene , 71 ★

#### The real estate billionaire shoveled snow and delivered newspapers as a kid, and paid for Johns Hopkins University by teaching Hebrew and checking IDs outside the gym and library.

#### #69. Stevie Wonder , 75

#### The musical powerhouse was blinded as a child and grew up in an impoverished household in Detroit.

#### #70. Dwayne “The Rock” Johnson , 53

#### The Rock named his production company Seven Bucks as a reminder of a bleak time: cut from the Canadian Football League, he arrived broke in Tampa with “a five, a one and change.”

#### #71. Norm Asbjornson , 90 ★

#### Asbjornson grew up in a home without electricity or running water before founding HVAC giant AAON.

#### #72. Leon G. Cooperman , 82 ★

#### The son of working-class immigrant parents, the hedge fund billionaire grew up in the Bronx.

#### #73. Edwin Chen , 38 ★

#### Chen worked in his parents’ small restaurant and attended MIT before building Surge AI into a multibillion-dollar company without any outside investment.

#### #74. J. Joe Ricketts , 84 ★

#### The TD Ameritrade founder’s first job at age 8 was cleaning bathrooms in his hometown in rural Nebraska.

#### #75. Marvin Ellison , 61

#### The Lowe’s CEO’s parents were tenant farmers. He worked his way from Target security guard to executive.

#### #76. Mary J. Blige , 55

#### The Grammy winner lived in a Yonkers housing project before a karaoke performance propelled her to stardom.

#### #77. José Hernandez , 63

#### The former NASA astronaut spent his childhood picking fruit and didn’t learn English until he was 12.

#### #78. Robert Johnson , 79 ★

#### The BET cofounder was raised in a working-class household with nine siblings and supported himself through college.

#### #79. Eminem , 53

#### Raised by a single mother in housing projects, Eminem was evicted from his apartment the day before he flew to Los Angeles to compete in the Rap Olympics, which led to his discovery by Dr. Dre.

#### #80. J. Wayne Weaver , 90 ★

#### The retail fashion mogul grew up in public housing before running Nine West.

#### #81. Jensen Huang , 63 ★

#### A Taiwan native who lived in Thailand as a child, Nvidia’s cofounder was sent to the U.S. amid civil unrest and inadvertently shipped to a reform school in Kentucky.

#### #82. Archie Emmerson , 96 ★

#### Two of his father’s sawmills burned to the ground when he was a child. His parents divorced, and Dad moved to California. Emmerson later joined him there, and together they built a sawmill—but his father’s heavy drinking nearly destroyed it. It eventually became Sierra Pacific Industries.

#### #83. Alice Walker , 82

#### The Color Purple ’s Pulitzer Prize-winning author grew up in a shack in the Jim Crow South; her parents were sharecroppers.

#### #84. Jerry Seinfeld , 71 ★

#### The comedian was raised by working-class parents in Long Island and spent years grinding at comedy clubs before sitcom stardom.

#### #85. Raj Sardana , 66 ★

#### The IT billionaire spent his childhood in a 225-square foot, government-provided one-bedroom in India with no heat, refrigeration or phone. He came to Georgia Tech in the 1980s with $100.

#### #86. Pharrell Williams , 52

#### Clap along for the hitmaker who’s happy now having survived a childhood marred by disconnected utilities and evictions.

#### #87. Gary Tharaldson , 80 ★

#### A former gym teacher from a 100-person town in North Dakota, he bought his first Super 8 motel in 1982.

#### #88. Leonardo DiCaprio , 51

#### The Oscar-winning actor was raised by a single mother in a rough neighborhood, littered with drugs; he famously faced dozens of rejections before landing his first acting gig in a commercial.

#### #89. Todd Christopher , 63 ★

#### The high-school dropout opened a hair salon at age 22, sleeping on its floor to save money, and later started Vogue International, with hair care brands including OGX, which he sold in 2014.

#### #90. Katalin Karikó , 71

#### The Nobel Prize-winning scientist grew up in a one-room home in Hungary without running water.

#### #91. Jerry Yang , 57 ★

#### Raised by a single mother, the Yahoo founder spoke little English when he immigrated at age 10.

#### #92. John Morgan , 69 ★

#### One of America’s premier trial lawyers, Morgan started working as a young teen to help support his family.

#### #93. Theresia Gouw , 57 ★

#### The billionaire venture capitalist was a child of refugees who waited tables and washed dishes to survive.

#### #94. Tom Golisano , 84 ★

#### The son of a seamstress and macaroni salesman, the payroll billionaire made money as a kid hauling newspapers to the dump.

#### #95. Herb Simon , 91 ★

#### The mall developer was raised in a Bronx walk-up, the son of a Jewish tailor from Central Europe.

#### #96. Patrick Soon-Shiong , 73 ★

#### The world’s richest doctor was born in apartheid South Africa to Chinese immigrants where, despite being a top student, he had to get government permission to work and earned 50% what his peers made.

#### #97. Mike Repole , 57 ★

#### The parents of the billionaire behind sports drink BodyArmor were Italian immigrants who worked as a waiter and seamstress.

#### #98. Alan Gerry , 97 ★

#### Gerry dropped out of high school to serve in World War II and studied TV repair before founding Cablevision.

#### #99. Kavitark Ram Shriram , 69 ★

#### One of Google’s first investors, Shriram lost his father at age 3 and immigrated to America with little.

#### #100. Willie Nelson , 92

#### The country star was abandoned by his parents and picked cotton before playing honky-tonks as a teen.

## #101-150

#101-150

#### ★ = BILLIONAIRE

#### #101. Eren Ozmen , 67 ★

#### The Turkish immigrant, who arrived with nearly nothing, sold baklava and cleaned offices to pay for her education.

#### #102. Kenny Troutt , 78 ★

#### The son of a single mother who worked as a bartender, Troutt grew up in public housing in Mount Vernon, Illinois. His fortune comes from Excel Communications, which he sold in 1998.

#### #103. Jewel , 51

#### The singer-songwriter grew up in a one-room Alaskan cabin and once lived in her van.

#### #104. Serena Williams , 44

#### The most dominant player in tennis history rose from the public courts of a working-class neighborhood in Compton, California.

#### #105. Hilary Swank , 51

#### The Oscar winner and her mom spent time living in a trailer park and in their car.

#### #106. Jennifer Hudson , 44

#### Raised by a single mother on Chicago’s South Side, the EGOT winner hit it big thanks to American Idol .

#### #107. Marian Ilitch , 93 ★

#### The daughter of working-class immigrants, the Little Caesars cofounder and her husband paid Rosa Parks’ rent for over a decade.

#### #108. Terrence Pegula , 74 ★

#### The son of a truck driver and miner, Pegula turned a $7,500 loan into a multibillion-dollar oil company.

#### #109. Max Levchin , 50 ★

#### The PayPal cofounder immigrated with his family as refugees from Soviet Ukraine and learned to speak English from watching television.

#### #110. Vincent Viola , 70 ★

#### A truck driver’s son, the financier rose from the trading pits to start his own firm.

#### #111. Glenn Dubin , 68 ★

#### The first in his family to attend college, the hedge fund billionaire played football for Stony Brook University before becoming a stockbroker.

#### #112. Bill Austin , 84 ★

#### The hearing aid billionaire spent his childhood scrounging for bottles to recycle to help his family make ends meet.

#### #113. Bruce Kovner , 81 ★

#### The hedge fund titan was raised by Eastern European immigrants who struggled through the Depression. He was a taxi driver before going into finance.

#### #114. Gary Michelson , 77 ★

#### He left home at 17, supporting himself through med school before inventing the medical devices that made him a billionaire.

#### #115. Bill Cummings , 89 ★

#### The real-estate developer grew up in a one-bedroom apartment above a liquor store.

#### #116. George Joseph , 104 ★

#### The son of a coal miner, America’s oldest billionaire grew up during the Great Depression.

#### #117. Jahm Najafi , 62 ★

#### After immigrating to the U.S. as a child, the investor grew up in a one-bedroom apartment in Phoenix.

#### #118. John Morris , 77 ★

#### The Bass Pro founder got his start selling fishing tackle out of his dad’s Ozarks-area liquor store.

#### #119. Chad Richison , 55 ★

#### The Paycom founder worked on his family farm before working through college.

#### #120. Evan Williams , 53 ★

#### The cofounder of Blogger, Medium and Twitter spent his childhood on a Nebraska farm.

#### #121. Tony Xu , 41 ★

#### As a kid, the DoorDash founder washed dishes in the restaurant where his mother worked as a waitress.

#### #122. James Clark , 81 ★

#### The Netscape founder dropped out of high school and joined the Navy to escape a turbulent childhood.

#### #123. Mariah Carey , 57

#### Carey grew up in poverty on Long Island and was a waitress before a demo got her a record deal.

#### #124. 50 Cent , 50

#### Curtis Jackson, whose drug-dealing mom died when he was young, started dealing himself at age 12 before making it as a rapper.

#### #125. Herriot Tabuteau , 57 ★

#### Born in Haiti, where his birth mother struggled to raise him, the biotech billionaire recalls experiencing “physical, nutritional, emotional” neglect.

#### #126. Jamie Kern Lima , 48

#### Given up at birth and adopted, the cosmetics mogul bagged groceries and coached gymnastics as a teen. The first in her family to go to college, she waitressed at Denny’s to pay her way.

#### #127. Al Pacino , 85

#### The Oscar and Tony winner was a high school dropout and briefly homeless.

#### #128. Omani Carson , 61 ★

#### The son of an alcoholic, sometimes abusive father, at age 17 he watched his overleveraged parents go bankrupt, then made his own fortune in financial advising.

#### #129. Gerald Ford , 81 ★

#### The banking billionaire grew up as a Texas farmboy and was the first in his family to attend college.

#### #130. Cher , 79

#### Raised by a struggling, itinerant single mother, Cher dropped out of high school before breaking into music.

#### #131. Byron Trott , 67 ★

#### The founder of merchant bank BDT launched a clothing store at 17 in his working-class neighborhood.

#### #132. Travis Boersma , 55 ★

#### With his late brother, Boersma started Dutch Bros as a coffee cart after his family sold its failing dairy farm.

#### #133. Alan B. Miller , 88 ★

#### The founder of healthcare provider UHS grew up in a cramped apartment behind his family’s dry-cleaning shop.

#### #134. Rick Workman , 71 ★

#### Workman went from hard labor on the family farm to becoming the nation’s richest dentist. (see “Meet The Billionaire Dentist That Other Docs Want To Punch In The Teeth”)

#### #135. Glen Taylor , 84 ★

#### The founder of printing giant Taylor Corp. grew up poor in Minnesota and worked as a laborer on his neighbor’s farms for a dollar an hour.

#### #136. Dan Wilks , 69 ★

#### His family of seven lived in a three-room goat shed; their dad taught himself masonry to build them a home and eventually went into that business.

#### #137. Farris Wilks , 74 ★

#### Dan’s brother and business partner, they sold their fracking business in 2011 for $3.5 billion. Farris is also a pastor.

#### #138. Michael Hsing , 65 ★

#### A foreign exchange student from China, Hsing came with little money and even less English. After struggling in school, he learned he had a learning disability that he overcame to eventually start semiconductor company MPS.

#### #139. Ronald Wanek , 84 ★

#### Wanek grew up on a struggling dairy farm before turning Ashley Furniture into America’s biggest furniture company.

#### #140. Richard Hayne , 78 ★

#### With only $4,000, the former hippie opened the first Urban Outfitters in Philadelphia with his ex-wife in the 1970s. He’s still CEO of the $5.6 billion (revenue) retailer.

#### #141. Andy Konwinski , 42 ★

#### The son of a machinist and a part-time grocery clerk, he was raised as a Jehovah’s Witness. When he began questioning some beliefs he was expelled from the faith, blocked by family members and reportedly talked about killing himself. He channeled his curiosity into co-founding Databricks and Perplexity.

#### #142. Sundar Pichai , 53 ★

#### Google’s current CEO slept in the living room of his family’s two-room apartment in India.

#### #143. Herb Chambers , 84 ★

#### Chambers grew up in working-class Dorchester, Massachusetts, collected carts at a supermarket, and dropped out of high school to join the Navy. He later borrowed $500 from his mom to open his first business before making a fortune in car dealerships.

#### #144. Emma Grede , 43

#### The serial fashion entrepreneur and chief product officer of Skims was raised in an East London high-rise by a single mother.

#### #145. John Hope Bryant , 60

#### Raised in a poor Compton neighborhood, the Operation HOPE founder was homeless before launching his first business venture.

#### #146. Jim Clayton , 91

#### The mobile home mogul grew up in a Tennessee log cabin; his family were tenant farmers on the property.

#### #147. W. Michael Blumenthal , 100

#### The Jewish refugee from Nazi Germany survived the Shanghai Ghetto before emigrating to the U.S., where he eventually became President Jimmy Carter’s Treasury Secretary.

#### #148. Eduardo Vivas , 40 ★

#### A high school dropout, Vivas packed bags in a warehouse before founding Bright.com, which was acquired by LinkedIn for $120 million. A pre-IPO investor in AppLovin, he still holds 2% in the tech firm.

#### #149. Tope Awotona , 44 ★

#### His family immigrated after his father died in a carjacking; Awotona founded Calendly by maxing out his credit cards.

#### #150. Fred Luddy , 71 ★

#### The ServiceNow founder ran away from home at 16 and picked strawberries to make money while he taught himself computer programming.

## #151-200

#151-200

#### ★ = BILLIONAIRE

#### #151. Tracy Chapman , 60

#### The Grammy winner was raised by a working-class single mother in Cleveland and started her career busking in coffeehouses.

#### #152. Dean Solon , 61 ★

#### The renewable energy titan got his start fixing people’s air conditioners as a teenager.

#### #153. Edward Lampert , 63 ★

#### The hedge fund billionaire’s father passed away when he was 14, throwing the family into financial disarray.

#### #154. Marc Lasry , 65 ★

#### Lasry immigrated from Morocco as a child, living in a tiny apartment before founding Avenue Capital.

#### #155. Kendrick Lamar , 38

#### The Grammy and Pulitzer winner’s family was homeless for a time and relied on food stamps before he broke big.

#### #156. Lauren Leichtman , 76 ★

#### The San Diego Wave owner started working as a teenager and supported herself through college working as a file clerk, bank teller, waitress and cashier.

#### #157. Lloyd Blankfein , 71 ★

#### The former chairman and CEO of Goldman Sachs grew up in a public housing project in Brooklyn.

#### #158. Kamal Ghaffarian , 67 ★

#### His uncle lent him $2,000 when he left Iran to study in the U.S. Ghaffarian parked cars at night to repay him before building a company whose spacecraft landed on the Moon.

#### #159. Jim Kavanaugh , 63 ★

#### The son of a bricklayer played soccer in the Olympics before cofounding IT giant World Wide Technology with David Steward.

#### #160. Dan Kurzius , 54 ★

#### Raised by a single mother after his father’s death, he was a part-time DJ and former competitive skateboarder who’d bluffed about his coding skills before cofounding Mailchimp.

#### #161. Charles Zegar , 78 ★

#### The son of a New York City subway conductor, Zegar is considered the software wizard behind Bloomberg’s terminals.

#### #162. Mark Bradford , 64

#### The award-winning artist grew up in a boarding house with his mother and attended art school in his 30s.

#### #163. Sheryl Swoopes , 54

#### Raised by a single mother in a small rural town, the WNBA star has won four championships and three Olympic golds.

#### #164. Kareem Abdul-Jabbar , 78

#### The NBA star and bestselling author rose from New York’s Dyckman Street Projects.

#### #165. Sheila Johnson , 77 ★

#### Her parents secretly sent their fair-skinned daughter to an all-white school before desegregation was fully implemented. When her father later abandoned the family, the BET cofounder struggled to keep the household together.

#### #166. Cardi B , 33

#### Raised in a low-income Bronx neighborhood, she worked as a stripper to fund her early music career.

#### #167. Viet Thanh Nguyen , 55

#### The Pulitzer Prize-winning author of The Sympathizer fled to America as a refugee in 1975, and lived for a time in a camp for Vietnamese refugees. His parents later opened one of the first Vietnamese grocery stores in San Jose, California.

#### #168. Venus Williams , 45

#### She was the first Black woman ranked No. 1 in tennis’ Open era.

#### #169. Thomas Tull , 55 ★

#### The Legendary Entertainment founder grew up in poverty with a single mother, attending college on a football scholarship.

#### #170. Simone Biles , 29

#### The Olympic Gold Medalist spent part of her childhood in the foster care system before being adopted by her grandparents.

#### #171. Tom Gores , 61 ★

#### Gores’ family of eight immigrated from Israel with just $40 and two suitcases; he briefly worked for brother Alec before starting his own PE firm and building a fortune that’s four times as big as Alec’s.

#### #172. Alec Gores , 72 ★

#### The billionaire founder of The Gores Group got his first job bagging groceries for 25 cents an hour at his uncle’s Flint, Michigan, store.

#### #173. Ron Burkle , 73 ★

#### Burkle made a fortune engineering turnarounds of major grocery brands with lessons learned from his father, a grocery store manager.

#### #174. Mark Jones , 64 ★

#### The insurance tycoon supported his family as a truck driver before earning his MBA.

#### #175. Dwight Schar , 84 ★

#### His single mother raised him in rural Ohio. His company NVR survived early bankruptcy to become a real estate giant.

#### #176. Kelcy Warren , 70 ★

#### Pipeline company Energy Transfer’s billionaire founder spent summers sweeping floors and working as a welder’s assistant.

#### #177. Ric Elias , 58 ★

#### Elias moved from Puerto Rico to the U.S. for college, paying for it with a mix of scholarships, loans and help from his dad. A survivor of the “Miracle on the Hudson” flight, he cofounded media company Red Ventures, which owns brands like The Points Guy, Bankrate and Lonely Planet.

#### #178. Ken Kendrick , 82 ★

#### The son of a gas station owner in West Virginia is now the managing general partner of the Arizona Diamondbacks.

#### #179. Sidney Kimmel , 98 ★

#### Born to a cab driver during the Great Depression, Kimmel dropped out of college before eventually founding Jones Apparel Group.

#### #180. Henry Swieca , 68 ★

#### The son of Holocaust survivors knocked on doors to get his first Wall Street job before founding his hedge fund.

#### #181. Norman Braman , 93 ★

#### The Braman Motorcars founder grew up in a blue-collar family and worked as the Philadelphia Eagles’ waterboy to help fund his education.

#### #182. Jed McCaleb , 51 ★

#### Raised in Arkansas by a single mother, the cryptocurrency mogul founded the first major bitcoin exchange.

#### #183. Jeff Tangney , 53 ★

#### Doximity’s founder spent his teens washing dishes at Pizza Hut.

#### #184. Janice Bryant Howroyd , 73

#### Howroyd grew up as one of 11 children in the Jim Crow South and got a full scholarship to college; she later started staffing firm ActOne Group with $1,500, including a $900 loan from her mom.

#### #185. Sylvester Stallone , 79

#### His mother tried to abort him. He was born with facial nerve damage and spent some of his earliest years in foster care before becoming a star thanks to the ultimate underdog movie, Rocky .

#### #186. Gary Friedman , 68 ★

#### The father of Restoration Hardware’s CEO passed away when he was 5 and his mother struggled with schizophrenia.

#### #187. Halle Berry , 59

#### The Academy Award-winning actress was raised by a single mother and lived in a homeless shelter in her 20s.

#### #188. Kieu Hoang , 81

#### A poor Vietnamese refugee, Hoang worked his way up the ladder at Abbott before founding his first healthcare company, RAAS, in 1980.

#### #189. David Sokol , 69

#### After his mom’s cancer diagnosis, Sokol started working odd jobs and later became a top executive at multiple energy companies.

#### #190. Bryan Stevenson , 66

#### Stevenson endured segregation in childhood, but it was his grandfather’s murder in his home when Stevenson was 16 that led him to become a lawyer who has spent his life defending poor and marginalized people, winning multiple Supreme Court victories.

#### #191. Fei-Fei Li , 49

#### The “godmother of AI” arrived in the U.S. at age 15 with her mother, who had just $20 in her pocket.

#### #192. Daymond John , 57

#### The FUBU founder and Shark Tank judge came from a working-class neighborhood in Queens, starting his career by sewing hats in his mother’s basement.

#### #193. Don Vultaggio , 74 ★

#### Before cofounding Arizona Beverages, the Brooklynite sold beer and soda out of a van in neighborhoods distributors wouldn’t enter.

#### #194. Jim Sinegal , 90

#### The Costco cofounder and son of a steel mill worker was bagging groceries for a living when he met his mentor, warehouse retail pioneer Sol Price.

#### #195. Carol Burnett , 92

#### Burnett, whose parents both suffered from addiction, was raised by her grandmother in a tiny studio apartment.

#### #196. Thomas Dundon , 54 ★

#### The Carolina Hurricanes owner grew up working class in New Jersey before building a fortune in subprime auto lending.

#### #197. Mitchell Morgan , 71 ★

#### The real estate developer’s father went bankrupt for the second time when Morgan was in 11th grade. He worked at his dad’s one remaining shoe store to pay his way through Temple University.

#### #198. Nick Caporella , 90 ★

#### The coal miner’s son started in construction before turning LaCroix into a category-defining sparkling water brand.

#### #199. Andrew Cherng , 78 ★

#### The son of a chef, Cherng came to the U.S. to attend Kansas’ Baker University. He worked as a waiter during summers and later opened a sit-down Chinese restaurant with his dad before launching mall-based Panda Express.

#### #200. Peggy Cherng , 78 ★

#### Also an immigrant, Cherng met her husband at Baker. She later gave up a career in electrical engineering to help build and run Panda Express.

## #201-250

#201-250

#### ★ = BILLIONAIRE

#### #201. Willis Johnson , 78 ★

#### Johnson moved his family into a trailer to buy a junkyard, laying the foundation for his multibillion-dollar auction company, Copart.

#### #202. Mary West , 80

#### With college out of reach, West was a secretary before cofounding a telemarketing powerhouse in her garage.

#### #203. John Catsimatidis , 77 ★

#### The Greek immigrant went from bagging groceries to owning a grocery store, building it into a chain and then diversifying.

#### #204. Mark Cuban , 67 ★

#### The Broadcast.com cofounder and Shark Tank shark sold stamps door-to-door as a kid and gave disco lessons to help pay his way through Indiana University. Later on, he shared a cramped apartment with five roommates where he slept on the floor. Recalls Cuban, “None of us had any money, but we had some wild times.”

#### #205. Mary C. Daly , 63

#### The San Francisco Federal Reserve CEO was a high school dropout who worked in a donut shop before pursuing her economics degree.

#### #206. Victor Ambros , 72

#### Ambros grew up on a subsistence dairy farm before attending MIT and making his Nobel Prize-winning discovery of microRNA.

#### #207. Ardem Patapoutian , 58

#### The Nobel Prize winner was held captive during Lebanon’s Civil War before emigrating; he later delivered pizza to support his biology education.

#### #208. Theodore Leonsis , 70 ★

#### The owner of the NHL’s Washington Capitals and NBA’s Washington Wizards was raised by working-class parents in a rough-and-tumble Brooklyn neighborhood.

#### #209. Brad Kelley , 69 ★

#### The farm boy dropped out of Western Kentucky University (four times, reportedly) but had more luck launching a discount cigarette firm, selling it and becoming a prominent landowner.

#### #210. Jessica Chastain , 49

#### The Oscar-winning actress recalls going to bed hungry—and her family stealing food to survive.

#### #211. David Rubenstein , 76 ★

#### The son of a postal clerk, the current Baltimore Orioles owner got a scholarship to Duke before working in the Carter Administration and cofounding private equity giant Carlyle.

#### #212. Peter Cancro , 68 ★

#### As a teenager, Cancro borrowed money from a former football coach to buy the deli where he worked and later transformed it into the national Jersey Mike’s chain.

#### #213. Ursula Burns , 67

#### Burns grew up in public housing and later became an intern at Xerox, rising in the ranks to become CEO.

#### #214. Joseph Neubauer , 84

#### At age 14, his parents put him on a boat headed for the U.S. so that he could have more opportunities than they did. The only English he spoke he learned from John Wayne movies. He eventually became CEO of Aramark.

#### #215. Karim Atiyeh , 36 ★

#### The fintech billionaire was taken hostage at gunpoint at the Syrian border when trying to leave Lebanon for his college exams; he later made it to Harvard and in 2019 cofounded Ramp.

#### #216. Misty Copeland , 43

#### The trailblazing ballerina spent part of her childhood living in a cramped motel room, living off food stamps.

#### #217. Kendra Scott , 51

#### As a newly single mother, Scott launched her eponymous jewelry business from a spare bedroom with $500.

#### #218. Earl Stafford , 77

#### One of 12 children whose dad worked in a Campbell Soup factory and whose mom was a housekeeper, Stafford sold hot dogs and sodas as a child to help his family before later founding Unitech.

#### #219. Jonny Kim , 42

#### After his father was shot and killed by police during a domestic incident when he was 16, Kim joined the Navy and later became an astronaut; he’s a strong contender to be one of the Artemis crew that returns to the moon.

#### #220. Selena Gomez , 33

#### The actress and beauty mogul was raised by a teenage mother who scrounged for quarters to pay for gas. She has publicly talked about her own bipolar disorder.

#### #221. Anastasia Soare , 68

#### Born in Romania, Soare immigrated to Los Angeles in 1989. As a 32-year-old single mother, unable to speak English or get approval for a credit card, she started out as an aesthetician, and later built an eyebrow-shaping empire.

#### #222. Thomas Mueller , 65 ★

#### The son of a logger, Mueller spent summers logging to pay for college at nearby University of Idaho before joining SpaceX as its first employee; he now runs his own rocket startup.

#### #223. Qasar Younis , 44 ★

#### The Pakistani-born son of Detroit auto factory workers sold his first company to Google and now works to make every vehicle self-driving.

#### #224. Marcia Taylor , 82

#### Taylor, who had three kids by age 19, escaped an abusive marriage. With her second husband, she turned a struggling trucking company into a logistics powerhouse called Bennett.

#### #225. Jesmyn Ward , 47

#### The award-winning author of Sing, Unburied, Sing was raised by a single mother who worked as a maid after a divorce.

#### #226. Katy Perry , 41

#### The Grammy-award winner whose religious family relied on food banks to survive sold her catalog for $225 million.

#### #227. Jimmy John Liautaud , 62 ★

#### Money was tight for Liautaud’s family, whose dad filed twice for bankruptcy. His dyslexia made school tough but he found success with his Jimmy John’s sandwich chain.

#### #228. Thomas Monaghan , 89

#### Monaghan spent his childhood in an orphanage and foster care before starting Domino’s with a $900 loan.

#### #229. George Argyros , 89 ★

#### Argyros worked as a paperboy to help his struggling family and started his real estate empire with a $1,200 loan.

#### #230. Mellody Hobson , 56

#### After a childhood marked by evictions and repossessions, Hobson rose from intern to co-CEO of multibillion-dollar money manager, Ariel Investments.

#### #231. Stephen King , 78

#### King was raised by a single mother and lived in a trailer in his 20s before selling his novel Carrie .

#### #232. Anousheh Ansari , 59

#### Her father lost everything after the Iranian Revolution; the Telecom Technologies cofounder spoke no English when she came to the U.S.

#### #233. Thasunda Brown Duckett , 52

#### As a child, the TIAA CEO’s family moved from New Jersey to Texas with only what fit in their car.

#### #234. Rosalind Brewer , 63

#### The child of General Motors assembly line workers, she was CEO of Sam’s Club and then Walgreens during Covid; she is now interim president of her alma mater, Spelman College.

#### #235. John O'Keefe , 86

#### The Nobel Prize-winning neuroscientist is the child of two immigrant shipyard laborers.

#### #236. Jack Dongarra , 75

#### The pioneering computer scientist was born to an immigrant father with little education; Dongarra also overcame dyslexia as a child.

#### #237. Martyna Majok , 41

#### The Pulitzer Prize-winning playwright’s childhood was funded by her mother’s factory and cleaning jobs.

#### #238. Robyn Jones , 63 ★

#### Married right after high school, Jones raised six children while her truck driver husband went to college. Frustrated with his road warrior lifestyle, she founded her own business, which became Goosehead Insurance.

#### #239. Mary Barra , 64

#### GM’s CEO got her start on the factory floor at age 18 and climbed its corporate ladder to the top rung.

#### #240. Ken Frazier , 71

#### The venture capitalist and former Merck CEO was raised by a single father who worked as a janitor.

#### #241. Therese Tucker , 64

#### Raised on a small farm, the youngest of four girls, Tucker worked as an engineer, then cashed out her savings to found fintech firm BlackLine.

#### #242. Ginni Rometty , 68

#### IBM’s legendary former CEO lived on food stamps as a child while her single mother struggled to make ends meet.

#### #243. Jasper Johns , 95

#### The iconic artist spent his childhood in rural South Carolina being shuffled between relatives after his parents’ divorce.

#### #244. Shyam Sankar , 44 ★

#### Born to immigrant parents whose dry cleaning business went bankrupt, Sankar is now Palantir’s CTO.

#### #245. David Green , 84

#### Green picked cotton to help his struggling family before leveraging a $600 loan to found what became retailer Hobby Lobby.

#### #246. Barbara Corcoran , 77

#### Raised in a two-bedroom apartment with nine siblings, the Shark Tank celebrity built her first multimillion-dollar business with a $1,000 loan.

#### #247. Phaedra Ellis-Lamkins , 49

#### The cofounder of payment platform Promise was raised by a single mother who relied on welfare and food stamps.

#### #248. Nichole Mustard , 53

#### Credit Karma’s cofounder grew up in rural Ohio and worked service jobs to help pay for college.

#### #249. Denis Yarats , 38 ★

#### Born in Belarus, the Perplexity cofounder moved to the United States to study artificial intelligence.

#### #250. Martha Stewart , 84

#### The queen of entertaining, who put herself through Barnard by modeling, was a stockbroker before opening her catering business. Despite spending five months in prison, she continues to expand her lifestyle empire.

> ★ ★ ★

#### CREDITS

#### Edited by: Alex Knapp and Luisa Kroll

#### Reported by: Jessica Jacolbe and Chase Peterson-Withorn

#### Self-Made 250 Judges: DeAngela Burns-Wallace , CEO, Ewing Marion Kauffman Foundation; Keith Dunleavy , Founder, Inovalon; Rich Karlgaard , Former Publisher, Forbes ; Steven Klinsky , Founder and CEO, New Mountain Capital; Jim McKelvey , Cofounder, Square (now Block); Ryan Rippel , CEO, NextLadder Ventures

#### Historic Self-Made 250 Judges : Louis Hyman , Professor of Political Economy in History, The Johns Hopkins University; Abbylin Sellers , Professor of Public Policy, Pepperdine University

#### Additional reporting: Amy Feldman, Randall Lane, Katherine Love, Michael Noer, Kirk Ogunrinde, Michael Solomon

#### Editorial Operations: Justin Conklin, Francesca Walton

#### Creative Director: Alicia Hallett-Chan

#### Director of Photography: Robyn Selman

#### Art and Design Direction: Fernando Capeto

#### Art Director, Editorial Operations: Charles Brucaliere

#### Editorial Design: Philip Smith, Yunjia Yuan, Macy Sinreich

#### Photo Research: Gail Toivanen

#### Product Enablement Lead: Juman Nidal

#### Product: Traci Kalamajka, Sophie Richards

#### Product Design Adrienne Michalski, Sara Amato

#### Engineering: Tay Buley, Diab Al Sadi, Ahmad Abdelraheem, Ahmad Alshawakri

#### QA: Gevorg Arakelyan, Kristine Karapetyan

#### MORE FROM FORBES
Got a tip? Share confidential information with Forbes.Editorial StandardsReprints & Permissions
Alex Knapp is a senior editor covering healthcare, science, and cutting edge technology who joined Forbes in 2011. He's written dozens of profiles of entrepreneurs across a variety of fields and done deep dives into technological trends from superconductors to space travel to pharmaceuticals. He also co-authors the InnovationRX newsletter and edits the Under 30 lists for Science and Healthcare in both North America and Europe. He has a B.S. in biochemistry from WPI and a J.D. from the University of Kansas School of Law. Follow him across social media sites at @thealexknapp. Email him at aknapp@forbes.com

**I am an executive editor at Forbes overseeing in-depth news and feature coverage across multiple areas including billionaires, real estate, energy, retail and philanthropy. I’ve written and/or edited dozens of cover stories including those on Bernard Arnault, Jersey Mike’s founder John Cancro and Kylie Jenner. I’ve overseen investigations into Russian oligarchs, billionaires and shady entrepreneurs. I was also the longtime co-editor of our World’s Billionaires List and the Forbes 400 Richest Americans and launched our lists of the nation’s most successful self-made women, top immigrants and richest families.**

A public file copy is available at https://ppl-ai-public.s3.amazonaws.com/data/search/wandr/forbes-self-made-250/article_raw.md.

Requirements:
- The URL must contain content that directly contradicts the Forbes statement.

Write one JSON object per line to `results_forbes_250_errors.jsonl`:
{"item": { "error": "<error>" }, "url": "<source_url>", "excerpts": ["<verbatim_excerpt_1>", "<verbatim_excerpt_2>", "..."], "answer": { <...whatever fields the task implies to ask for...> }}
