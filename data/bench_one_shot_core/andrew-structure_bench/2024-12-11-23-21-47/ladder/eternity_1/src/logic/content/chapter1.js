export default {
  scenes: {
    void: {
      location: 'darkChamber',
      beats: {
        awakening: {
          lines: [
            {
              type: 'narration',
              text: 'Darkness envelops everything. A faint dripping sound echoes in the distance. Alex awakens on a cold, hard floor.'
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'thinking',
              text: 'Ugh... my head. Where am I?'
            },
            {
              type: 'narration',
              text: 'A soft whisper brushes past their ear.'
            },
            {
              type: 'dialog',
              speaker: 'whisper',
              variation: 'neutral',
              noSpeakerSprite: true,
              text: 'Awaken...'
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'surprised',
              text: "Who's there? Show yourself!"
            },
            {
              type: 'narration',
              text: 'Silence. Alex strains their eyes but sees nothing.'
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'thinking',
              text: 'Great. Just great. Lost in the dark with voices. Think, Alex, think.'
            }
          ],
          next: {
            chapter: 'chapter1',
            scene: 'void',
            beat: 'echoes'
          }
        },
        echoes: {
          lines: [
            {
              type: 'narration',
              text: 'Alex feels around, their hands sliding over damp walls.'
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'thinking',
              text: 'Feels like stone. Maybe an old building?'
            },
            {
              type: 'narration',
              text: 'A faint light flickers to the left; a distant sound echoes to the right.'
            },
            {
              type: 'choice',
              text: 'Which way should Alex go?',
              options: [
                {
                  text: 'Follow the faint light',
                  next: {
                    chapter: 'chapter1',
                    scene: 'void',
                    beat: 'followLight'
                  }
                },
                {
                  text: 'Follow the distant sound',
                  next: {
                    chapter: 'chapter1',
                    scene: 'void',
                    beat: 'followSound'
                  }
                }
              ]
            }
          ]
        },
        followLight: {
          lines: [
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'neutral',
              text: "Light means a way out. Let's hope that's true."
            },
            {
              type: 'narration',
              text: 'They move cautiously towards the flickering glow.'
            }
          ],
          next: {
            chapter: 'chapter1',
            scene: 'fork',
            beat: 'lightPath'
          }
        },
        followSound: {
          lines: [
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'neutral',
              text: 'Maybe that sound is someone who can help.'
            },
            {
              type: 'narration',
              text: 'They head towards the sound, footsteps echoing.'
            }
          ],
          next: {
            chapter: 'chapter1',
            scene: 'fork',
            beat: 'soundPath'
          }
        }
      }
    },
    fork: {
      location: 'symbolChamber',
      beats: {
        lightPath: {
          lines: [
            {
              type: 'narration',
              text: 'Alex enters a chamber illuminated by strange symbols.'
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'surprised',
              text: 'What is this place?'
            },
            {
              type: 'narration',
              text: 'A figure steps out of the shadows.'
            },
            {
              type: 'dialog',
              speaker: 'mysteriousFigure',
              variation: 'neutral',
              text: "You've finally arrived."
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'surprised',
              text: 'Who are you?'
            },
            {
              type: 'dialog',
              speaker: 'mysteriousFigure',
              variation: 'neutral',
              text: 'A friend. Perhaps more.'
            }
          ],
          next: {
            chapter: 'chapter1',
            scene: 'fork',
            beat: 'trustOrDoubt'
          }
        },
        soundPath: {
          lines: [
            {
              type: 'narration',
              text: 'Alex finds themselves in a corridor with flickering lights. A radio crackles nearby.'
            },
            {
              type: 'dialog',
              speaker: 'radioVoice',
              variation: 'neutral',
              noSpeakerSprite: true,
              text: 'Is someone there?'
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'surprised',
              text: "Yes! I'm here! Who is this?"
            },
            {
              type: 'dialog',
              speaker: 'radioVoice',
              variation: 'neutral',
              noSpeakerSprite: true,
              text: 'Help is on the way. Trust no one.'
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'surprised',
              text: 'Wait, what do you mean?'
            }
          ],
          next: {
            chapter: 'chapter1',
            scene: 'fork',
            beat: 'trustOrDoubt'
          }
        },
        trustOrDoubt: {
          lines: [
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'thinking',
              text: "This is getting weirder by the minute."
            },
            {
              type: 'narration',
              text: 'Footsteps approach.'
            },
            {
              type: 'dialog',
              speaker: 'stranger',
              variation: 'neutral',
              text: 'You look lost.'
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'neutral',
              text: "That's an understatement."
            },
            {
              type: 'dialog',
              speaker: 'stranger',
              variation: 'neutral',
              text: 'Come with me. I can help.'
            },
            {
              type: 'choice',
              text: 'What should Alex do?',
              options: [
                {
                  text: 'Trust the stranger and follow them',
                  next: {
                    chapter: 'chapter1',
                    scene: 'fork',
                    beat: 'trust'
                  }
                },
                {
                  text: 'Doubt their intentions and stay back',
                  next: {
                    chapter: 'chapter1',
                    scene: 'fork',
                    beat: 'doubt'
                  }
                }
              ]
            }
          ]
        },
        trust: {
          lines: [
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'neutral',
              text: 'Alright. Lead the way.'
            },
            {
              type: 'dialog',
              speaker: 'stranger',
              variation: 'neutral',
              text: 'Wise decision.'
            },
            {
              type: 'narration',
              text: 'They walk together down a dimly lit hallway.'
            }
          ],
          next: {
            chapter: 'chapter1',
            scene: 'shadows',
            beat: 'exploration'
          }
        },
        doubt: {
          lines: [
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'neutral',
              text: "I think I'll manage on my own."
            },
            {
              type: 'dialog',
              speaker: 'stranger',
              variation: 'neutral',
              text: "Suit yourself. Don't say I didn't warn you."
            },
            {
              type: 'narration',
              text: 'The stranger fades into the darkness.'
            }
          ],
          next: {
            chapter: 'chapter1',
            scene: 'shadows',
            beat: 'exploration'
          }
        }
      }
    },
    shadows: {
      location: 'corridor',
      beats: {
        exploration: {
          lines: [
            {
              type: 'narration',
              text: 'Alone, Alex continues exploring.'
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'thinking',
              text: "Maybe I should've gone with them."
            },
            {
              type: 'narration',
              text: 'They stumble upon a wall covered in drawings.'
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'thinking',
              text: 'These symbols... why do they feel familiar?'
            },
            {
              type: 'narration',
              text: 'A sudden pain flashes in their head.'
            },
            {
              type: 'dialog',
              speaker: 'whisper',
              variation: 'neutral',
              noSpeakerSprite: true,
              text: 'Remember...'
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'surprised',
              text: 'Ah! What was that?'
            }
          ],
          next: {
            chapter: 'chapter1',
            scene: 'shadows',
            beat: 'fightOrFlight'
          }
        },
        fightOrFlight: {
          lines: [
            {
              type: 'narration',
              text: 'A shadowy figure emerges behind them.'
            },
            {
              type: 'dialog',
              speaker: 'shadowyFigure',
              variation: 'neutral',
              text: "You shouldn't be here."
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'surprised',
              text: 'Who are you?'
            },
            {
              type: 'dialog',
              speaker: 'shadowyFigure',
              variation: 'neutral',
              text: 'Your end.'
            },
            {
              type: 'choice',
              text: 'What should Alex do?',
              options: [
                {
                  text: 'Stand and fight',
                  next: {
                    chapter: 'chapter1',
                    scene: 'shadows',
                    beat: 'fight'
                  }
                },
                {
                  text: 'Run away',
                  next: {
                    chapter: 'chapter1',
                    scene: 'shadows',
                    beat: 'flee'
                  }
                }
              ]
            }
          ]
        },
        fight: {
          lines: [
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'angry',
              text: "I'm not afraid of you!"
            },
            {
              type: 'narration',
              text: 'They clench their fists, ready to defend themselves.'
            }
          ],
          next: {
            chapter: 'chapter1',
            scene: 'awakening',
            beat: 'timeStop'
          }
        },
        flee: {
          lines: [
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'surprised',
              text: 'Nope! Not dealing with this!'
            },
            {
              type: 'narration',
              text: 'Alex turns and sprints down the corridor.'
            }
          ],
          next: {
            chapter: 'chapter1',
            scene: 'awakening',
            beat: 'timeStop'
          }
        }
      }
    },
    awakening: {
      location: 'symbolChamber',
      beats: {
        timeStop: {
          lines: [
            {
              type: 'narration',
              text: 'Regardless of the choice, the ground trembles. Time seems to slow.'
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'surprised',
              text: "What's happening?"
            },
            {
              type: 'narration',
              text: 'Objects around them float as if suspended.'
            },
            {
              type: 'dialog',
              speaker: 'mysteriousFigure',
              variation: 'neutral',
              text: "It's awakening within you."
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'surprised',
              text: 'What is?'
            },
            {
              type: 'dialog',
              speaker: 'mysteriousFigure',
              variation: 'neutral',
              text: 'Your true power.'
            }
          ],
          next: {
            chapter: 'chapter1',
            scene: 'awakening',
            beat: 'finalChoice'
          }
        },
        finalChoice: {
          lines: [
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'surprised',
              text: 'My... power?'
            },
            {
              type: 'dialog',
              speaker: 'mysteriousFigure',
              variation: 'neutral',
              text: 'Yes. The ability to manipulate time itself.'
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'surprised',
              text: "This can't be real."
            },
            {
              type: 'choice',
              text: 'What should Alex do?',
              options: [
                {
                  text: 'Embrace the power',
                  next: {
                    chapter: 'chapter2',
                    scene: 'aftermath',
                    beat: 'initial'
                  }
                },
                {
                  text: 'Reject the power',
                  next: {
                    chapter: 'chapter2',
                    scene: 'aftermath',
                    beat: 'initial'
                  }
                }
              ]
            }
          ]
        }
      }
    }
  }
}
