import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { PlayerCard } from "@/components/ui/custom/player/player_card"

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
  collections: {
    creatures: Creature[]
  }
}

interface GameUIData {
  entities: {
    player: Player
    opponent: Player
    player_creature?: Creature
    opponent_creature?: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const { player, opponent, player_creature, opponent_creature } = props.data.entities

  // Safety check - if no creatures are present, show loading or error state
  if (!player_creature || !opponent_creature) {
    return (
      <div className="flex items-center justify-center h-screen w-full">
        <p>Loading battle...</p>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-screen w-full max-w-[177.78vh] mx-auto aspect-video bg-background">
      {/* HUD */}
      <div className="flex justify-between items-center h-[10%] px-4 bg-muted/20">
        {player && (
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
          />
        )}
        <div className="flex gap-4">
          <Sword className="w-6 h-6" />
          <Shield className="w-6 h-6" />
          <Zap className="w-6 h-6" />
        </div>
        {opponent && (
          <PlayerCard
            uid={opponent.uid}
            name={opponent.display_name}
          />
        )}
      </div>

      {/* Battlefield */}
      <div className="flex justify-between items-center h-[60%] px-16 py-8">
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            currentHp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
          />
          <span className="mt-2 text-sm font-semibold">Your Creature</span>
        </div>

        <div className="flex flex-col items-center">
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            currentHp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
          />
          <span className="mt-2 text-sm font-semibold">Opponent's Creature</span>
        </div>
      </div>

      {/* Action UI */}
      <div className="h-[30%] p-4 bg-muted/10">
        <div className="grid grid-cols-2 gap-4 h-full">
          {player_creature.collections?.skills?.map((skill) => (
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
