import { Shield, Swords } from 'lucide-react'
import { useCurrentButtons } from "@/lib/useChoices"
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    base_damage: number
    [key: string]: any
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
    opponent: Player
    player_creature: Creature
    opponent_creature: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data?.entities?.player_creature
  const opponentCreature = props.data?.entities?.opponent_creature

  if (!playerCreature || !opponentCreature || 
      playerCreature.__type !== "Creature" || 
      opponentCreature.__type !== "Creature") {
    return <div>Loading battle...</div>
  }

  return (
    <div className="h-screen w-screen aspect-video flex flex-col">
      {/* HUD */}
      <nav className="h-[10%] bg-slate-800 flex items-center justify-between px-4">
        <div className="flex items-center gap-2 text-white">
          <Shield className="h-6 w-6" />
          <span>Battle Scene</span>
        </div>
        <div className="flex items-center gap-2 text-white">
          <Swords className="h-6 w-6" />
        </div>
      </nav>

      {/* Battlefield */}
      <div className="h-[60%] grid grid-cols-2 gap-4 p-8 bg-slate-200">
        <div className="flex items-center justify-center">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            currentHp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl={`/creatures/${playerCreature.meta?.prototype_id || 'default'}.png`}
          />
        </div>
        <div className="flex items-center justify-center">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            currentHp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
            imageUrl={`/creatures/${opponentCreature.meta?.prototype_id || 'default'}.png`}
          />
        </div>
      </div>

      {/* UI Area */}
      <div className="h-[30%] bg-slate-100 p-4 overflow-y-auto">
        <div className="grid grid-cols-2 gap-4">
          {playerCreature.collections?.skills?.map(skill => {
            if (skill.__type !== "Skill") return null
            
            return (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={skill.stats}
              />
            )
          })}
        </div>
      </div>
    </div>
  )
}
