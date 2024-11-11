import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { PlayerCard } from "@/components/ui/custom/player/player_card"

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    damage: number
  }
}

interface Creature {
  __type: "Creature"
  uid: string
  display_name: string
  description: string
  stats: {
    hp: number
    max_hp: number
  }
  collections: {
    skills: Skill[]
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  description: string
  collections: {
    creatures: Creature[]
  }
}

interface GameUIData {
  entities: {
    player: Player
    bot: Player
    player_creature: Creature
    bot_creature: Creature
  }
  collections: {
    queued_skills: Skill[]
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const { player, bot, player_creature, bot_creature } = props.data?.entities || {}

  if (!player || !bot || !player_creature || !bot_creature) {
    return <div className="text-center p-4">Loading battle...</div>
  }

  const handleSkillClick = (skillUid: string) => {
    if (availableButtonSlugs?.includes(skillUid)) {
      emitButtonClick(skillUid)
    }
  }

  const skills = player_creature.collections?.skills || []

  return (
    <div className="h-screen w-screen bg-background">
      <div className="container mx-auto aspect-video">
        <div className="grid grid-rows-[auto_1fr_auto] h-full">
          {/* Top HUD */}
          <div className="flex justify-between items-center p-4 bg-muted">
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl="/placeholder-player.png"
            />
            <div className="flex items-center gap-2">
              <Shield className="w-6 h-6" />
              <span>Battle Scene</span>
            </div>
            <PlayerCard
              uid={bot.uid}
              name={bot.display_name}
              imageUrl="/placeholder-bot.png"
            />
          </div>

          {/* Battlefield */}
          <div className="flex justify-between items-center px-8 py-4">
            <div className="relative">
              <CreatureCard
                uid={player_creature.uid}
                name={player_creature.display_name}
                hp={player_creature.stats.hp}
                maxHp={player_creature.stats.max_hp}
                imageUrl="/placeholder-creature.png"
                className="relative"
              />
              <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 bg-primary text-primary-foreground px-3 py-1 rounded-full">
                Player
              </div>
            </div>

            <Swords className="w-8 h-8" />

            <div className="relative">
              <CreatureCard
                uid={bot_creature.uid}
                name={bot_creature.display_name}
                hp={bot_creature.stats.hp}
                maxHp={bot_creature.stats.max_hp}
                imageUrl="/placeholder-creature.png"
                className="relative"
              />
              <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 bg-destructive text-destructive-foreground px-3 py-1 rounded-full">
                Opponent
              </div>
            </div>
          </div>

          {/* Skills UI */}
          <div className="p-4 bg-muted">
            <div className="grid grid-cols-4 gap-4">
              {skills.length > 0 ? (
                skills.map((skill: Skill) => (
                  <SkillButton
                    key={skill.uid}
                    uid={skill.uid}
                    name={skill.display_name}
                    description={skill.description}
                    stats={`Damage: ${skill.stats.damage}`}
                    disabled={!availableButtonSlugs?.includes(skill.uid)}
                    onClick={() => handleSkillClick(skill.uid)}
                  />
                ))
              ) : (
                <div className="col-span-4 text-center text-muted-foreground">
                  No skills available
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
