import { Shield, Swords } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { useCurrentButtons } from "@/lib/useChoices"

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    base_damage: number
  }
  meta: {
    prototype_id: string
    category: string
    skill_type: string
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
    attack: number
    defense: number
    speed: number
  }
  meta: {
    prototype_id: string
    category: string
    creature_type: string
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
  meta: {
    prototype_id: string
    category: string
  }
  collections: {
    creatures: Creature[]
  }
}

interface GameUIData {
  entities: {
    player: Player
    opponent: Player
    player_creature: Creature
    opponent_creature: Creature
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
  const opponentCreature = props.data?.entities?.opponent_creature

  if (!playerCreature || !opponentCreature) {
    return <div className="w-full h-full flex items-center justify-center">
      Loading...
    </div>
  }

  return (
    <div className="h-full w-full aspect-[16/9] flex flex-col bg-slate-900 text-white">
      {/* HUD */}
      <div className="h-16 bg-slate-800 flex items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <Shield className="h-6 w-6" />
          <span>Battle Scene</span>
        </div>
        <div className="flex items-center gap-2">
          <Swords className="h-6 w-6" />
        </div>
      </div>

      {/* Battlefield */}
      <div className="flex-1 grid grid-cols-2 gap-8 items-center px-12">
        <div className="flex justify-center">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            currentHp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl={`/creatures/${playerCreature.meta.prototype_id}.png`}
          />
        </div>
        <div className="flex justify-center">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            currentHp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
            imageUrl={`/creatures/${opponentCreature.meta.prototype_id}.png`}
          />
        </div>
      </div>

      {/* UI Controls */}
      <div className="h-1/4 bg-slate-700 p-4 flex flex-col gap-4">
        <div className="grid grid-cols-2 gap-4">
          {playerCreature.collections?.skills?.map((skill: Skill) => (
            skill && (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                damage={skill.stats.base_damage}
              />
            )
          ))}
        </div>
      </div>
    </div>
  )
}
