import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"

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
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player_creature
  const botCreature = props.data.entities.bot_creature

  const handleSkillClick = (skillSlug: string) => {
    if (availableButtonSlugs.includes(skillSlug)) {
      emitButtonClick(skillSlug)
    }
  }

  const getSkillSlug = (skill: Skill) => {
    return `skill:${skill.uid}`
  }

  return (
    <div className="min-h-screen w-full flex flex-col bg-background">
      {/* HUD */}
      <nav className="h-16 bg-primary flex items-center justify-between px-4 z-10">
        <div className="flex items-center gap-2">
          <Shield className="h-6 w-6" />
          <span className="font-bold text-primary-foreground">Battle Arena</span>
        </div>
        <Swords className="h-6 w-6" />
      </nav>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center px-8 py-4">
        {playerCreature && (
          <div className="flex flex-col items-center gap-2">
            <span className="text-sm font-bold">Your Creature</span>
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
              imageUrl={`/creatures/${playerCreature.display_name.toLowerCase()}.png`}
            />
          </div>
        )}

        {botCreature && (
          <div className="flex flex-col items-center gap-2">
            <span className="text-sm font-bold">Opponent's Creature</span>
            <CreatureCard
              uid={botCreature.uid}
              name={botCreature.display_name}
              hp={botCreature.stats.hp}
              maxHp={botCreature.stats.max_hp}
              imageUrl={`/creatures/${botCreature.display_name.toLowerCase()}.png`}
            />
          </div>
        )}
      </div>

      {/* Controls */}
      <div className="min-h-[200px] bg-secondary p-4 rounded-t-lg">
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4 justify-items-center">
          {playerCreature?.collections.skills.map(skill => {
            const skillSlug = getSkillSlug(skill)
            return (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.damage}`}
                disabled={!availableButtonSlugs.includes(skillSlug)}
                onClick={() => handleSkillClick(skillSlug)}
              />
            )
          })}
        </div>
      </div>
    </div>
  )
}
