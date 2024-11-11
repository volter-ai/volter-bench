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
    base_damage: number
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
  }
  collections: {
    skills?: Skill[]
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  collections: {
    creatures?: Creature[]
  }
}

interface GameUIData {
  entities: {
    player?: Player
    opponent?: Player
    player_creature?: Creature
    opponent_creature?: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities?.player_creature
  const opponentCreature = props.data.entities?.opponent_creature

  if (!playerCreature || !opponentCreature) {
    return <div className="w-full h-full aspect-video bg-background flex items-center justify-center">
      <p>Loading battle...</p>
    </div>
  }

  return (
    <div className="w-full h-full aspect-video bg-background flex flex-col">
      {/* Top HUD */}
      <nav className="w-full p-4 bg-secondary/10">
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-2">
            <Swords className="h-5 w-5" />
            <span>{playerCreature.display_name} vs {opponentCreature.display_name}</span>
          </div>
          <div className="flex items-center gap-2">
            <Shield className="h-5 w-5" />
            <span>Battle</span>
          </div>
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center px-12 py-6">
        <div className="relative">
          <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-sm font-bold">
            Your Creature
          </span>
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            currentHp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl={`/assets/creatures/${playerCreature.meta?.prototype_id || 'default'}.png`}
          />
        </div>

        <div className="relative">
          <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-sm font-bold">
            Opponent's Creature
          </span>
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            currentHp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
            imageUrl={`/assets/creatures/${opponentCreature.meta?.prototype_id || 'default'}.png`}
          />
        </div>
      </div>

      {/* Skills/UI Area */}
      <div className="bg-secondary/10 p-6">
        <div className="grid grid-cols-2 gap-4 max-w-md mx-auto">
          {playerCreature.collections?.skills?.map((skill) => {
            if (skill.__type !== "Skill") return null;
            
            return (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                damage={skill.stats?.base_damage}
              />
            );
          })}
        </div>
      </div>
    </div>
  )
}
