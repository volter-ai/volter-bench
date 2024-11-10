import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Swords } from 'lucide-react'
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
  __type: "MainGameScene"
  entities: {
    player: Player
    bot: Player
    player_creature: Creature
    bot_creature: Creature
  }
  stats: Record<string, never>
  meta: Record<string, never>
  collections: {
    queued_skills: never[]
  }
  uid: string
  display_name: string
  description: string
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data?.entities?.player_creature
  const botCreature = props.data?.entities?.bot_creature

  if (!playerCreature || !botCreature) {
    return <div className="h-full w-full aspect-video flex items-center justify-center bg-slate-900">
      <p className="text-slate-200">Loading battle...</p>
    </div>
  }

  return (
    <div className="h-full w-full aspect-video flex flex-col bg-slate-900">
      <nav className="h-16 bg-slate-800 flex items-center px-4 border-b border-slate-700">
        <div className="flex items-center gap-2">
          <Swords className="h-6 w-6 text-slate-200" />
          <span className="text-slate-200 font-bold">Battle Arena</span>
        </div>
      </nav>

      <main className="flex-grow flex justify-between items-center px-8">
        <div className="relative">
          <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-slate-200 font-bold">
            Your Creature
          </span>
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl={`/creatures/${playerCreature.meta.prototype_id}.png`}
          />
        </div>

        <div className="relative">
          <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-slate-200 font-bold">
            Opponent's Creature
          </span>
          <CreatureCard
            uid={botCreature.uid}
            name={botCreature.display_name}
            hp={botCreature.stats.hp}
            maxHp={botCreature.stats.max_hp}
            imageUrl={`/creatures/${botCreature.meta.prototype_id}.png`}
          />
        </div>
      </main>

      <footer className="h-48 bg-slate-800 p-4 border-t border-slate-700">
        <div className="flex flex-wrap gap-2">
          {playerCreature.collections.skills?.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
          {(!playerCreature.collections.skills || playerCreature.collections.skills.length === 0) && (
            <p className="text-slate-400">No skills available</p>
          )}
        </div>
      </footer>
    </div>
  )
}
