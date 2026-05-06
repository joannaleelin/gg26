// Per-person info-sheet content extracted from .docx files in
// /Individual Assignments/. Keyed by slug (lowercase, hyphenated name).
//
// Schema:
//   role_title           string  — shows under the name on detail page
//   staff_call_time      string  — e.g. "2:00 PM" — fills the first timeline row
//   assignments          array of { phase, time, role, location, role_leader }
//   assignment_notes     array of strings — optional bullets after the assignments table
//   role_descriptions    array of role blocks, each with:
//                          title, summary, what_youll_do (array of strings),
//                          partner_info (string or { heading, items: [] }),
//                          guest_info (string or array of strings),
//                          lead_name, lead_phone, lead_tel
//   additional_contacts  array of { name, role, phone, tel }
//   ideal_break          string — e.g. "7:45 - 8:30 PM"

const STANDARD_CONTACTS = [
  { name: "Joanna Lin",  role: "Staffing Lead",              phone: "734-674-6795", tel: "+17346746795" },
  { name: "Linda Chu",   role: "Production / Gifting Lead",  phone: "860-398-0834", tel: "+18603980834" },
  { name: "Rose Yan",    role: "EVP Marketing & Growth",     phone: "323-381-8898", tel: "+13233818898" },
];

window.GG_INFO_SHEETS = {

  "ada-lee": {
    role_title: "PHOTO/VIDEO LEAD",
    staff_call_time: "2:00 PM",
    assignments: [
      { phase: "Pre-Event",                time: "2:30–4:30 PM",   role: "Follow Photo/Video",                                                              location: "—",     role_leader: "Ada Lee — (713) 628-1389" },
      { phase: "Cocktails",                time: "4:30–6:30 PM",   role: "Photo/Video Manager - Float",                                                     location: "Float", role_leader: "Ada Lee — (713) 628-1389" },
      { phase: "Transition to Dinner",     time: "6:20–7:00 PM",   role: "Move to JMP to manage photo/video during transition to dinner; ensure all house/photo move to positions", location: "Float", role_leader: "—" },
      { phase: "Dinner & Program",         time: "7:00–9:30 PM",   role: "Photo/Video Manager - Float",                                                     location: "Float", role_leader: "Ada Lee — (713) 628-1389" },
      { phase: "Transition to Afterparty", time: "~9:30–10:00 PM", role: "Ensure all house/photo move",                                                     location: "Float", role_leader: "—" },
      { phase: "Founders Party",           time: "10:00 PM–1:00 AM", role: "Photo/Video Manager - Float",                                                   location: "Float", role_leader: "Ada Lee — (713) 628-1389" },
    ],
    assignment_notes: [
      "As you are listed as the Role Leader, if any issues arise, you should ping Joanna or Rose for help!",
      "To wrap-up, please notify Joanna that you're done for the evening. If you have a walkie/radio, please return it to the Gold House Production office.",
    ],
    role_descriptions: [
      {
        title: "PHOTO/VIDEO LEAD — Cocktails / Dinner & Program / Founders Party",
        summary: "The Photo/Video Lead accompanies house photographers to ensure shot lists are captured.",
        what_youll_do: [
          "Particularly important for partner activations (OpenTable logo, SmartWater bottles on tables)",
          "Focus on VVIP guests mingling at their tables, especially unexpected pairings (e.g. Priyanka + Eileen Gu)",
          "Focus on the first two rows and center tables where VVIPs are seated",
          "Let the photographer ask for photos — they are experienced. Don't engage talent directly",
        ],
        partner_info: {
          heading: "Partner Photographers Onsite",
          items: [
            "Hennessy (via LEDE): 1 Getty, 1 BFA, 1 Roaming — focused solely on their activations",
            "Genesis: 3 Getty — 1 at Grand Arrivals (no stairs), 1 at GoldBot, 1 roaming during cocktails (all 3 wrap upon conclusion of cocktails)",
            "OpenTable: 2 social videographers capturing Debby Soo arrival, at cocktails, during program, as well as BTS of Gala dinner prep during 6p–7p",
          ],
        },
        guest_info: "VVIP tables are priority. Let the photographer lead — don't engage talent directly.",
        lead_name: "Ada Lee",
        lead_phone: "(713) 628-1389",
        lead_tel: "+17136281389",
      },
    ],
    additional_contacts: STANDARD_CONTACTS,
    ideal_break: "7:45 - 8:30 PM",
  },

  "daniel-park": {
    role_title: "CONTENT/SOCIAL",
    staff_call_time: "1:00 PM",
    assignments: [
      { phase: "Pre-Event",                time: "2:30–4:30 PM",   role: "Social Team Prep",                              location: "—",                role_leader: "Joseph Kim — (201) 693-7482" },
      { phase: "Cocktails",                time: "4:30–6:30 PM",   role: "Social - Gold Carpet",                          location: "Gold Carpet",      role_leader: "Joseph Kim — (201) 693-7482" },
      { phase: "Transition to Dinner",     time: "6:20–7:00 PM",   role: "Social - JMP guests sitting down",              location: "—",                role_leader: "—" },
      { phase: "Dinner & Program",         time: "7:00–9:30 PM",   role: "Social - Program starting at 8 PM",             location: "JMP - Program",    role_leader: "Joseph Kim — (201) 693-7482" },
      { phase: "Transition to Afterparty", time: "~9:30–10:00 PM", role: "Social - Dinner guests mingling",               location: "—",                role_leader: "—" },
      { phase: "Founders Party",           time: "10:00 PM–1:00 AM", role: "Social - Roaming until 11:30 PM",             location: "—",                role_leader: "Joseph Kim — (201) 693-7482" },
    ],
    role_descriptions: [
      {
        title: "SOCIAL — Cocktails / Dinner & Program / Founders Party",
        summary: "The Social team captures content of the assigned zone throughout the evening.",
        what_youll_do: [
          "Each social staffer owns one zone: Gold Stairs, Press Carpet/Photo Pit, Cocktail Reception (roaming), Founders Room, Backstage, Program (on-stage), DSL Portraits, Kanya Portraits, or VIP Portraits (Chase reel)",
          "Capture partner deliverables per shot list",
          "Stop capture if talent uncomfortable",
          "Get group photo of each honoree/presenter before stage",
          "Hand raw content to Post-Production team",
        ],
        partner_info: "Hennessy, Maybelline, SmartWater, OpenTable, L'Oréal, Chase Sapphire — see shot list docs for specifics.",
        guest_info: "Stop capture if talent uncomfortable. Get a group photo of each honoree/presenter before stage.",
        lead_name: "Joseph Kim",
        lead_phone: "(201) 693-7482",
        lead_tel: "+12016937482",
      },
    ],
    additional_contacts: STANDARD_CONTACTS,
    ideal_break: "7:00 - 7:45 PM",
  },

  "allie-woo": {
    role_title: "TALENT & PORTRAIT STUDIO SUPPORT",
    staff_call_time: "11:00 AM",
    assignments: [
      { phase: "Pre-Event",                time: "2:30–4:30 PM",   role: "No assignment",                                  location: "—",                       role_leader: "—" },
      { phase: "Cocktails",                time: "4:30–6:30 PM",   role: "Talent Wrangler - End of Carpet",                location: "Grand Ave",               role_leader: "Rebecca Chin — (267) 253-4998" },
      { phase: "Transition to Dinner",     time: "6:20–7:00 PM",   role: "Move to VIP Portraits",                          location: "—",                       role_leader: "Pooja Kumar — (832) 643-1186" },
      { phase: "Dinner & Program",         time: "7:00–9:30 PM",   role: "VIP Portrait Lounge Support",                    location: "VIP Portrait Lounge",     role_leader: "Pooja Kumar — (832) 643-1186" },
      { phase: "Transition to Afterparty", time: "~9:30–10:00 PM", role: "Wrap-up",                                        location: "—",                       role_leader: "—" },
      { phase: "Founders Party",           time: "10:00 PM–1:00 AM", role: "No assignment",                                location: "—",                       role_leader: "—" },
    ],
    assignment_notes: [
      "No formal assignment during Founders Party. Feel free to enjoy the event — and remember you're still representing Gold House. Stay reachable in case your Lead needs you.",
      "To wrap-up, please notify Pooja or Joanna that you're done for the evening. If you have a walkie/radio, please return it to the Gold House Production office.",
    ],
    role_descriptions: [
      {
        title: "TALENT WRANGLERS – PRESS LINE — END OF CARPET — during Cocktails",
        summary: "The Talent Wrangler (End of Press Line) cohort receives on-stage talent as they come off the carpet and escorts them to the Founders Room — the talent holding room on the second floor of the Dorothy Chandler Pavilion. This role is for on-stage talent only.",
        what_youll_do: [
          "Station yourself at the end of the carpet and receive on-stage talent as they come off the press line",
          "As you walk with them toward the Founders Room, you will pass by the GlamBot station — ask if they'd like to participate. If yes, they are allowed to cut the line. Christina Garvin is stationed at the GlamBot and will take it from there.",
          "Once they are done with the GlamBot (or if they choose to skip it), escort them directly to the Founders Room on the 2nd floor of the Dorothy Chandler Pavilion",
          "There is a Smart Water station at the end of the press line — offer a drink as you receive each guest, but don't push if they decline",
        ],
        partner_info: {
          heading: "Important partner info",
          items: [
            "Smart Water is a hydration sponsor — there is a station at the end of the press line; offer to on-stage talent as they come off the carpet",
            "Genesis GlamBot is stationed along the route — Christina Garvin manages this activation; on-stage talent may cut the line if they wish to participate",
          ],
        },
        guest_info: [
          "This role is for on-stage talent only — do not pull or escort any other guests",
          "These guests have just come off the press line and may need a moment; be warm and give them space to breathe as you walk with them",
          "GlamBot is entirely optional — offer it, but follow their lead and don't linger if they want to move on",
        ],
        lead_name: "Rebecca Chin",
        lead_phone: "(267) 253-4998",
        lead_tel: "+12672534998",
      },
      {
        title: "VIP PORTRAIT LOUNGE — INSIDE TEAM — during Transition to Dinner / Dinner & Program",
        summary: "The VIP Portrait Lounge team manages the full guest experience inside the lounge during cocktail hour, directing guests to their designated studio and making sure the space feels warm, welcoming, and well-stocked.",
        what_youll_do: [
          "When a guest arrives, check the list and direct them to either the Portrait Studio (Kanya) or the Content Studio (Tiffany's team)",
          "If there is a line for either studio, invite the guest to sit and relax while they wait — make sure they feel taken care of",
          "Ensure food, water, and snacks are available and stocked in the lounge at all times. Two Sequoia team members are managing room cleanup and drink refills — flag them if anything needs refreshing.",
          "Smart Water bottles should be available in the lounge for hydration",
          "L'Oréal has a touch-up station with a makeup artist in the lounge — you don't need to push guests toward it, but let them know it's available",
          "If a guest wants a drink, let the servers know",
          "Once a guest has completed their studio experience, direct them back to cocktails",
          "Exception: a very small number of guests — board members only — are eligible to be escorted to the Founders Room after their experience. You will have a list. If a board member does not want to go to the Founders Room, that is completely fine — direct them to cocktails as usual.",
          "Once the program is over, all operations end",
        ],
        partner_info: {
          heading: "Important partner info",
          items: [
            "Chase Sapphire is the exclusive sponsor of the VIP Portrait Lounge — all Chase branded products and materials should be properly set and looking good throughout the event",
            "L'Oréal has a touch-up station and makeup artist in the lounge — no pressure for guests to use it, but make them aware; the L'Oréal branded mirror should remain set up and visible",
            "Smart Water: bottles should be stocked and available for guests in the lounge at all times",
          ],
        },
        guest_info: [
          "Guests will have received advance communications about this experience — you do not need to over-explain",
          "If there is a wait, keep the atmosphere relaxed and comfortable — guests should feel like VIPs, not like they're standing in line",
          "Board members only are eligible for Founders Room escort after their experience — you will have this list. If they decline, accept graciously and direct them to cocktails.",
          "If a guest wants a drink, alert the servers — do not let guests go without",
        ],
        lead_name: "Pooja Kumar",
        lead_phone: "(832) 643-1186",
        lead_tel: "+18326431186",
      },
    ],
    additional_contacts: STANDARD_CONTACTS,
    ideal_break: "7:45 - 8:30 PM",
  },

};
