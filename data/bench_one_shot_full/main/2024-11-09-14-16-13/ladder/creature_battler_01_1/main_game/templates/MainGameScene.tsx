import { Shield, Swords } from 'lucide-react'
import { CreatureCard } from '@/components/ui/custom/creature/creature_card'
import { SkillButton } from '@/components/ui/custom/skill/skill_button'
import { useCurrentButtons } from "@/lib/useChoices"

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
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player?.collections?.creatures?.[0]
  const botCreature = props.data.entities.bot?.collections?.creatures?.[0]

  if (!playerCreature || !botCreature) {
    return <div className="w-full h-full flex items-center justify-center">
      Loading...
    </div>
  }

  const handleSkillClick = (skillUid: string) => {
    emitButtonClick(skillUid)
  }

  const isSkillAvailable = (skillUid: string): boolean => {
    return Array.isArray(availableButtonSlugs) && availableButtonSlugs.includes(skillUid)
  }

  return (
    <div className="w-full min-h-screen flex flex-col">
      <nav className="h-16 w-full bg-primary flex items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <Shield className="h-6 w-6" />
          <span>Battle Arena</span>
        </div>
        <Swords className="h-6 w-6" />
      </nav>

      <div className="flex-1 flex justify-between items-center px-8 bg-background py-8">
        <div className="flex flex-col items-center gap-4">
          <span className="text-lg font-bold">Player</span>
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl={`/creatures/${playerCreature.display_name.toLowerCase()}.png`}
          />
        </div>

        <div className="flex flex-col items-center gap-4">
          <span className="text-lg font-bold">Opponent</span>
          <CreatureCard
            uid={botCreature.uid}
            name={botCreature.display_name}
            hp={botCreature.stats.hp}
            maxHp={botCreature.stats.max_hp}
            imageUrl={`/creatures/${botCreature.display_name.toLowerCase()}.png`}
          />
        </div>
      </div>

      <div className="min-h-[200px] bg-secondary p-4">
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4 auto-rows-max overflow-y-auto">
          {playerCreature.collections.skills?.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              disabled={!isSkillAvailable(skill.uid)}
              onClick={() => handleSkillClick(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
