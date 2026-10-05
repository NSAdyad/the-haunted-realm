// Echoes of the Past: the supplied twelve slides, preceded by one invitation.
// Source wording and record labels are preserved; emphasis is presentational only.
export const ECHOES_SLIDES = [
  {
    id: 'intro',
    title: 'Echoes of the Past',
    subtitle: 'Follow the lantern into the past',
    layout: 'intro',
    paragraphs: [
      'Step into the mist, follow the glow of the lantern, and let the shadows reveal their stories.'
    ],
    images: [{
      src: 'outputs/the-haunted-realm-echoes-navigation-image-review-v1.png',
      alt: 'An ancient roundhouse in cold mist, with an ember-lit doorway.',
      caption: ''
    }]
  },
  {
    id: 'samhain',
    source: '01-samhain.jpeg',
    title: 'Samhain',
    subtitle: '(SOW-IN)',
    layout: 'image-text',
    paragraphs: [
      'Ancient <strong>Celtic festival</strong> (around <strong>31st October</strong>).',
      'Marked the <strong>end of the harvest</strong> and the <strong>start of winter</strong> (the “dark half” of the year).',
      'It was a difficult time, as people faced <strong>cold, hunger and the possibility of death</strong>.',
      'Believed that the boundary between the world of the <strong>living and the dead</strong> became thinner, so spirits could return.',
      'People lit <strong>large fires</strong> for protection and made <strong>offerings to the gods</strong>.',
      'They wore <strong>costumes</strong> (often animal skins) to hide from spirits.'
    ],
    images: [{
      src: 'assets/echoes/bonfire.webp',
      alt: 'A large bonfire.',
      caption: 'Samhain'
    }],
    cycle: [
      { label: 'Samhain', text: '31st October' },
      { label: 'Yule', text: 'Winter Solstice' },
      { label: 'Imbolc', text: '1st February' },
      { label: 'Ostara', text: 'Spring Equinox' },
      { label: 'Beltane', text: '1st May' },
      { label: 'Litha', text: 'Summer Solstice' },
      { label: 'Lughnasadh', text: '1st August' },
      { label: 'Mabon', text: 'Autumn Equinox' }
    ]
  },
  {
    id: 'christianity-and-all-saints-day',
    source: '02-christianity-all-saints-day.jpeg',
    title: 'Christianity and All Saints’ Day',
    layout: 'timeline',
    paragraphs: [
      'Early Christian communities honoured <strong>martyrs and saints</strong>.',
      'Over time, <strong>All Saints’ Eve (31 October)</strong>, <strong>All Saints’ Day (1 November)</strong> and <strong>All Souls’ Day (2 November)</strong> became part of the Christian calendar.'
    ],
    timeline: [
      { label: '609', text: 'Pope Boniface IV dedicated the Pantheon in Rome to the Virgin Mary and all martyrs (13 May 609), establishing a feast of All Martyrs in the Western Church.' },
      { label: '8th century', text: 'Pope Gregory III expanded the celebration to all saints and associated it with 1 November.' },
      { label: '9th century', text: 'Pope Gregory IV extended the 1 November observance across the Western Church.' }
    ],
    images: [{
      src: 'assets/echoes/pantheon.webp',
      alt: 'The Pantheon in Rome.',
      caption: 'The Pantheon in Rome'
    }]
  },
  {
    id: 'halloween-the-name',
    source: '03-halloween-the-name.jpeg',
    title: 'Halloween — The Name',
    layout: 'flow',
    paragraphs: [
      'All Saints’ Day was also known as <strong>All Hallows’ Day</strong> or <strong>All-hallowmas</strong>.',
      'The evening before All Saints’ Day was called <strong>All Hallows’ Eve</strong>; over time, the name gradually became <strong>Halloween</strong>.',
      'Halloween is therefore linguistically connected to All Hallows’ Eve: the word <strong>hallow</strong> means <strong>‘saint’</strong>.',
      'Medieval Halloween customs included beliefs about the dead and supernatural beings, and people sometimes wore disguises or costumes. However, the reasons and practices <strong>varied by place and period</strong>.'
    ],
    flow: [
      { label: 'ALL HALLOWS', text: 'referring to all saints' },
      { label: 'ALL HALLOWS’ EVE', text: 'the evening before All Saints’ Day' },
      { label: 'HALLOWEEN', text: 'the name that gradually developed' }
    ],
    images: [{
      src: 'assets/echoes/vigil.webp',
      alt: 'A candlelit vigil.',
      caption: 'All Hallows’ Eve'
    }]
  },
  {
    id: 'the-legend-of-jack-o-lanterns',
    source: '04-jack-o-lanterns.jpeg',
    title: 'The Legend of Jack-o’-Lanterns',
    layout: 'image-text',
    paragraphs: [
      'The story of <strong>Stingy Jack</strong> is a popular <strong>Irish folktale</strong> associated with the jack-o’-lantern tradition.',
      'In one version, Jack repeatedly tricks the Devil, including trapping him in a tree, and later dies unable to enter Heaven or Hell.',
      'He is condemned to wander in darkness with a <strong>burning coal</strong>, which he carries in a <strong>hollowed turnip</strong>.',
      'Irish and Scottish traditions used <strong>carved turnips and other root vegetables</strong> as lanterns; the pumpkin became dominant in North America later.'
    ],
    images: [{
      src: 'assets/echoes/turnip.webp',
      alt: 'A carved turnip lantern.',
      caption: 'A hollowed turnip'
    }]
  },
  {
    id: 'pumpkins',
    source: '05-pumpkins.jpeg',
    title: 'Pumpkins',
    layout: 'flow',
    paragraphs: [
      'Irish and Scottish traditions used <strong>carved turnips and other root vegetables</strong> as lanterns; pumpkins became the dominant material in <strong>North America</strong> after immigrants brought the tradition.',
      'U.S. pumpkin production varies by year. The USDA reported <strong>1.44 billion pounds in 2024</strong> in its annual survey, while broader USDA estimates put total 2024 commercial production at around <strong>1.9 billion pounds</strong>.',
      'Pumpkin <strong>flowers, seeds and flesh</strong> are edible and rich in vitamins.',
      'Pumpkins are used in <strong>soups, desserts, breads</strong> and many other dishes.',
      'Carving pumpkins into <strong>jack-o’-lanterns</strong> is now a major Halloween tradition.'
    ],
    flow: [
      { label: 'TURNIP', text: 'Traditional lanterns in Ireland and Scotland' },
      { label: 'IMMIGRATION', text: 'The tradition brought to North America' },
      { label: 'PUMPKIN', text: 'Became dominant material in North America' }
    ],
    images: [{
      src: 'assets/echoes/harvest.webp',
      alt: 'A harvest of pumpkins.',
      caption: 'Pumpkins'
    }]
  },
  {
    id: 'halloween-celebrations',
    source: '06-halloween-celebrations.jpeg',
    title: 'Halloween Celebrations',
    layout: 'image-text',
    paragraphs: [
      'Halloween is celebrated in <strong>many countries around the world</strong>.',
      'In the <strong>United States</strong>, costumes, trick-or-treating, parties and community events are common.',
      'In <strong>Ireland</strong>, traditional celebrations have included bonfires, dressing up, games and visiting homes.',
      'Popular activities include <strong>costume parties, trick-or-treating, apple bobbing, games and spooky decorations</strong>.',
      'Celebrations <strong>vary greatly between countries and communities</strong>.'
    ],
    images: [{
      src: 'assets/echoes/celebrations.webp',
      alt: 'A Halloween celebration.',
      caption: 'Halloween Celebrations'
    }]
  },
  {
    id: 'trick-or-treating',
    source: '07-trick-or-treating.jpeg',
    title: 'Trick or Treating',
    layout: 'image-text',
    paragraphs: [
      'Modern trick-or-treating developed from <strong>several older European customs</strong>.',
      'In <strong>medieval England</strong>, <strong>‘souling’</strong> involved people visiting homes and receiving <strong>soul cakes</strong> in exchange for prayers for the dead.',
      'In <strong>Scotland and Ireland</strong>, <strong>‘guising’</strong> involved children dressing up and performing a song, poem, joke or other small ‘trick’ before receiving a treat.',
      'The phrase <strong>‘trick or treat’</strong> appeared in North America in the <strong>early 20th century</strong>, and the custom became widespread in the United States <strong>after the Second World War</strong>.',
      'Today, children commonly dress up, visit homes and ask for <strong>sweets or other treats</strong>.'
    ],
    images: [{
      src: 'assets/echoes/souling.webp',
      alt: 'People visiting a home during souling.',
      caption: 'Souling'
    }]
  },
  {
    id: 'halloween-events',
    source: '08-halloween-events.jpeg',
    title: 'Halloween Events',
    layout: 'image-text',
    paragraphs: [
      'Halloween events <strong>vary widely between countries and communities</strong>.',
      '<strong>Parades and costume events</strong> are common in some communities.',
      '<strong>Haunted houses and other haunted attractions</strong> became popular organised Halloween entertainment, especially in the United States.',
      '<strong>Pumpkin carving and pumpkin contests</strong> are popular seasonal activities in many places.',
      '<strong>Parties, games and community gatherings</strong> are also common.'
    ],
    images: [{
      src: 'assets/echoes/haunted-events.webp',
      alt: 'A Halloween haunted attraction.',
      caption: 'Halloween Events'
    }]
  },
  {
    id: 'pumpkin-records',
    source: '09-pumpkin-records.jpeg',
    title: 'Pumpkin Records',
    layout: 'comparison',
    paragraphs: [
      'The <strong>2025 record</strong> surpassed the <strong>2010 record</strong> by <strong>more than 1,000 lb</strong>.'
    ],
    comparison: [
      {
        label: '2010 — HISTORICAL RECORD',
        name: 'Chris Stevens (USA)',
        weight: '1,810.5 lb (821.2 kg)',
        location: 'Stillwater Harvest Fest, Minnesota',
        date: '9 October 2010',
        note: 'It was the world record at the time.'
      },
      {
        label: 'CURRENT WORLD RECORD',
        name: 'Ian & Stuart Paton (UK)',
        weight: '2,819 lb 4 oz (1,278.8 kg)',
        location: 'Wargrave, Berkshire',
        date: '6 October 2025',
        note: ''
      }
    ],
    images: [
      {
        src: 'assets/echoes/pumpkin-2010.webp',
        alt: 'Chris Stevens with the 2010 record pumpkin.',
        caption: '2010 — HISTORICAL RECORD'
      },
      {
        src: 'assets/echoes/pumpkin-2025.webp',
        alt: 'Ian and Stuart Paton with the 2025 record pumpkin.',
        caption: 'CURRENT WORLD RECORD'
      }
    ]
  },
  {
    id: '2010-world-record-pumpkin-pie',
    source: '10-giant-pumpkin-pie.jpeg',
    title: '2010 World Record Pumpkin Pie',
    layout: 'ingredients',
    paragraphs: [
      'On <strong>25 September 2010</strong>, the <strong>New Bremen Giant Pumpkin Growers</strong> made the <strong>Guinness World Records largest pumpkin pie</strong> at <strong>New Bremen Pumpkinfest</strong> in <strong>New Bremen, Ohio, USA</strong>.'
    ],
    facts: [
      { label: 'Weight', text: '1,678 kg (3,699 lb)' },
      { label: 'Diameter', text: '6 metres (20 ft)' },
      { label: 'Crust', text: '440 sheets of dough' }
    ],
    ingredients: [
      { label: 'Canned pumpkin', text: '1,212 lb' },
      { label: 'Evaporated milk', text: '109 US gallons' },
      { label: 'Eggs', text: '2,796 eggs (233 dozen)' },
      { label: 'Sugar', text: '525 lb' },
      { label: 'Salt', text: '7 lb' },
      { label: 'Cinnamon', text: '14.5 lb' },
      { label: 'Pumpkin spice', text: '' }
    ],
    images: [{
      src: 'assets/echoes/pie.webp',
      alt: 'The giant pumpkin pie at New Bremen Pumpkinfest.',
      caption: '2010 World Record Pumpkin Pie'
    }]
  },
  {
    id: 'most-lit-pumpkins',
    source: '11-most-lit-pumpkins.jpeg',
    title: 'Most Lit Pumpkins',
    layout: 'record',
    paragraphs: [
      'All the pumpkins had to be <strong>lit at the same time and in the same place</strong>.',
      'On <strong>October 26, 2007</strong>, <strong>Boston, Massachusetts</strong>, set the world record with <strong>30,128 lit pumpkins!</strong>',
      'The pumpkins were part of a <strong>community event</strong> and were arranged in a <strong>giant pyramid</strong>.'
    ],
    facts: [
      { label: 'WORLD RECORD', text: '30,128 LIT PUMPKINS' },
      { label: 'Location', text: 'Boston, Massachusetts, USA' },
      { label: 'Date', text: 'October 26, 2007' }
    ],
    images: [{
      src: 'assets/echoes/pyramid.webp',
      alt: 'A giant pyramid of lit pumpkins.',
      caption: '30,128 LIT PUMPKINS'
    }]
  },
  {
    id: 'fastest-pumpkin-carver',
    source: '12-fastest-pumpkin-carver.jpeg',
    title: 'Fastest Pumpkin Carver',
    layout: 'dual-profile',
    paragraphs: [
      'On <strong>October 31, 2013</strong>, <strong>Steve Clarke</strong> of <strong>Havertown, Pennsylvania (USA)</strong> carved a pumpkin in a record time of <strong>1 minute and 14.8 seconds</strong>.',
      '<strong>Jerry Ayers</strong> of <strong>Baltimore, Ohio (USA)</strong> set a world record in <strong>1999</strong> by carving <strong>one ton of pumpkins</strong> (with detailed designs) in <strong>7 hours and 11 minutes</strong>.'
    ],
    images: [
      {
        src: 'assets/echoes/carver-steve.webp',
        alt: 'Steve Clarke carving a pumpkin.',
        caption: 'Steve Clarke'
      },
      {
        src: 'assets/echoes/carver-jerry.webp',
        alt: 'Jerry Ayers carving a pumpkin.',
        caption: 'Jerry Ayers'
      }
    ]
  }
];
