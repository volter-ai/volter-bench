export default {
  scenes: {
    aftermath: {
      location: 'symbolChamber',
      beats: {
        initial: {
          lines: [
            {
              type: 'narration',
              text: 'Alex stands amidst a swirling vortex of energy.'
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'surprised',
              text: 'Did I just... stop time?'
            },
            {
              type: 'narration',
              text: 'A soft laugh emanates from behind.'
            },
            {
              type: 'dialog',
              speaker: 'luna',
              variation: 'neutral',
              text: "Impressive, isn't it?"
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'neutral',
              text: 'Who are you now?'
            },
            {
              type: 'dialog',
              speaker: 'luna',
              variation: 'neutral',
              text: "Names Luna. I've been watching you."
            }
          ],
          next: {
            chapter: 'chapter2',
            scene: 'aftermath',
            beat: 'strangerOffer'
          }
        },
        strangerOffer: {
          lines: [
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'thinking',
              text: "Watching me? That's not creepy at all."
            },
            {
              type: 'dialog',
              speaker: 'luna',
              variation: 'neutral',
              text: "There's much you don't understand. But I can help."
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'neutral',
              text: 'Why should I trust you?'
            },
            {
              type: 'dialog',
              speaker: 'luna',
              variation: 'neutral',
              text: 'Because we share the same gift.'
            },
            {
              type: 'choice',
              text: 'What should Alex do?',
              options: [
                {
                  text: 'Agree to go with Luna',
                  next: {
                    chapter: 'chapter2',
                    scene: 'aftermath',
                    beat: 'agreeWithLuna'
                  }
                },
                {
                  text: 'Decline and go alone',
                  next: {
                    chapter: 'chapter2',
                    scene: 'aftermath',
                    beat: 'decline'
                  }
                }
              ]
            }
          ]
        },
        agreeWithLuna: {
          lines: [
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'neutral',
              text: "Alright. I'm in."
            },
            {
              type: 'dialog',
              speaker: 'luna',
              variation: 'happy',
              text: 'Excellent. Follow me.'
            },
            {
              type: 'narration',
              text: 'They walk together into a shimmering portal.'
            }
          ],
          next: {
            chapter: 'chapter2',
            scene: 'depths',
            beat: 'withLuna'
          }
        },
        decline: {
          lines: [
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'neutral',
              text: "I think I'll figure this out myself."
            },
            {
              type: 'dialog',
              speaker: 'luna',
              variation: 'neutral',
              text: 'Very well. The offer stands if you change your mind.'
            },
            {
              type: 'narration',
              text: 'Luna disappears, leaving Alex alone.'
            }
          ],
          next: {
            chapter: 'chapter2',
            scene: 'depths',
            beat: 'alone'
          }
        }
      }
    },
    depths: {
      location: 'sanctuary',
      beats: {
        withLuna: {
          lines: [
            {
              type: 'narration',
              text: 'They arrive at an underground facility filled with others.'
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'surprised',
              text: 'What is this place?'
            },
            {
              type: 'dialog',
              speaker: 'luna',
              variation: 'neutral',
              text: 'Our sanctuary. A place for people like us.'
            },
            {
              type: 'dialog',
              speaker: 'elder',
              variation: 'neutral',
              text: "Welcome, Alex. We've been expecting you."
            }
          ],
          next: {
            chapter: 'chapter2',
            scene: 'depths',
            beat: 'mission'
          }
        },
        alone: {
          lines: [
            {
              type: 'narration',
              text: 'Alex wanders the streets, time glitches occur around them.'
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'thinking',
              text: 'These anomalies... What is causing them?'
            },
            {
              type: 'narration',
              text: 'An old newspaper catches their eye, mentioning time distortions.'
            }
          ],
          next: {
            chapter: 'chapter2',
            scene: 'depths',
            beat: 'mission'
          }
        },
        mission: {
          lines: [
            {
              type: 'dialog',
              speaker: 'elder',
              variation: 'neutral',
              text: 'We need your help to restore balance.'
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'neutral',
              text: 'Why me?'
            },
            {
              type: 'dialog',
              speaker: 'elder',
              variation: 'neutral',
              text: 'You have the potential to change everything.'
            },
            {
              type: 'choice',
              text: 'What should Alex do?',
              options: [
                {
                  text: 'Accept the mission',
                  next: {
                    chapter: 'chapter2',
                    scene: 'depths',
                    beat: 'acceptMission'
                  }
                },
                {
                  text: 'Decline and leave',
                  next: {
                    chapter: 'chapter2',
                    scene: 'depths',
                    beat: 'declineMission'
                  }
                }
              ]
            }
          ]
        },
        acceptMission: {
          lines: [
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'neutral',
              text: 'If I can help, I will.'
            },
            {
              type: 'dialog',
              speaker: 'elder',
              variation: 'happy',
              text: 'Your courage is commendable.'
            }
          ],
          next: {
            chapter: 'chapter2',
            scene: 'betrayal',
            beat: 'discovery'
          }
        },
        declineMission: {
          lines: [
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'neutral',
              text: "I didn't sign up for this."
            },
            {
              type: 'dialog',
              speaker: 'elder',
              variation: 'neutral',
              text: 'Destiny has a way of catching up.'
            }
          ],
          next: {
            chapter: 'chapter2',
            scene: 'betrayal',
            beat: 'discovery'
          }
        }
      }
    },
    betrayal: {
      location: 'facility',
      beats: {
        discovery: {
          lines: [
            {
              type: 'narration',
              text: 'As Alex delves deeper, they overhear a clandestine conversation.'
            },
            {
              type: 'dialog',
              speaker: 'voice1',
              variation: 'neutral',
              noSpeakerSprite: true,
              text: 'Tonight, we turn the tide.'
            },
            {
              type: 'dialog',
              speaker: 'voice2',
              variation: 'neutral',
              noSpeakerSprite: true,
              text: 'They suspect nothing.'
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'thinking',
              text: 'What are they plotting?'
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'thinking',
              text: 'I need to tell someone... but who can I trust?'
            },
            {
              type: 'choice',
              text: 'What should Alex do?',
              options: [
                {
                  text: 'Expose the conspiracy',
                  next: {
                    chapter: 'chapter2',
                    scene: 'betrayal',
                    beat: 'expose'
                  }
                },
                {
                  text: 'Keep it to themselves for now',
                  next: {
                    chapter: 'chapter2',
                    scene: 'betrayal',
                    beat: 'conceal'
                  }
                }
              ]
            }
          ]
        },
        expose: {
          lines: [
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'surprised',
              text: "There's a plot against us!"
            },
            {
              type: 'dialog',
              speaker: 'luna',
              variation: 'surprised',
              text: 'This is grave news.'
            },
            {
              type: 'dialog',
              speaker: 'elder',
              variation: 'neutral',
              text: 'We must act immediately.'
            }
          ],
          next: {
            chapter: 'chapter2',
            scene: 'rift',
            beat: 'beginning'
          }
        },
        conceal: {
          lines: [
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'thinking',
              text: 'I need more proof before I accuse anyone.'
            },
            {
              type: 'narration',
              text: 'They decide to investigate further.'
            }
          ],
          next: {
            chapter: 'chapter2',
            scene: 'rift',
            beat: 'beginning'
          }
        }
      }
    },
    rift: {
      location: 'streets',
      beats: {
        beginning: {
          lines: [
            {
              type: 'narration',
              text: 'The sky cracks open, revealing a swirling rift.'
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'surprised',
              text: 'What is that?!'
            },
            {
              type: 'dialog',
              speaker: 'luna',
              variation: 'neutral',
              text: "The temporal rift. It's worse than we feared."
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'neutral',
              text: 'How do we stop it?'
            },
            {
              type: 'dialog',
              speaker: 'luna',
              variation: 'neutral',
              text: 'We have to face it head-on.'
            },
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'thinking',
              text: 'Or find another way.'
            },
            {
              type: 'choice',
              text: 'What should Alex do?',
              options: [
                {
                  text: 'Confront the rift',
                  next: {
                    chapter: 'chapter2',
                    scene: 'rift',
                    beat: 'confront'
                  }
                },
                {
                  text: 'Escape to safety',
                  next: {
                    chapter: 'chapter2',
                    scene: 'rift',
                    beat: 'escape'
                  }
                }
              ]
            }
          ]
        },
        confront: {
          lines: [
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'angry',
              text: "I'm not running away. Let's end this."
            },
            {
              type: 'dialog',
              speaker: 'luna',
              variation: 'neutral',
              text: 'Together, then.'
            },
            {
              type: 'narration',
              text: 'They prepare to enter the rift.'
            }
          ],
          next: {
            isGameOver: true
          }
        },
        escape: {
          lines: [
            {
              type: 'dialog',
              speaker: 'alex',
              variation: 'neutral',
              text: 'We need to regroup. This is too big.'
            },
            {
              type: 'dialog',
              speaker: 'luna',
              variation: 'neutral',
              text: 'Time may not be on our side.'
            },
            {
              type: 'narration',
              text: 'They retreat as the rift expands.'
            }
          ],
          next: {
            isGameOver: true
          }
        }
      }
    }
  }
}
