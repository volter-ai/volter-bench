import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
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
    player_creature: Creature
    opponent_creature: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const { player, opponent, player_creature, opponent_creature } = props.data?.entities || {}

  return (
    <div className="w-full h-full aspect-video bg-slate-900 flex flex-col">
      {/* HUD */}
      <div className="h-1/6 bg-slate-800 flex items-center justify-between px-4">
        <div className="flex items-center gap-4">
          {player?.uid && (
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl="/placeholder-player.png"
            />
          )}
        </div>
        <div className="flex items-center gap-4">
          {opponent?.uid && (
            <PlayerCard
              uid={opponent.uid}
              name={opponent.display_name}
              imageUrl="/placeholder-opponent.png"
            />
          )}
        </div>
      </div>

      {/* Battlefield */}
      <div className="h-3/6 grid grid-cols-2 gap-8 p-8 bg-slate-700">
        <div className="flex items-center justify-center">
          {player_creature?.uid && player_creature.stats && (
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              currentHp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              imageUrl="/placeholder-creature.png"
            />
          )}
        </div>
        <div className="flex items-center justify-center">
          {opponent_creature?.uid && opponent_creature.stats && (
            <CreatureCard
              uid={opponent_creature.uid}
              name={opponent_creature.display_name}
              currentHp={opponent_creature.stats.hp}
              maxHp={opponent_creature.stats.max_hp}
              imageUrl="/placeholder-creature.png"
            />
          )}
        </div>
      </div>

      {/* Controls */}
      <div className="h-2/6 bg-slate-800 p-4">
        <div className="grid grid-cols-2 gap-4 h-full">
          {player_creature?.collections?.skills?.map((skill) => (
            skill?.uid && (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                damage={skill.stats?.base_damage}
                variant="secondary"
                className="h-full text-lg"
              />
            )
          ))}
        </div>
      </div>
    </div>
  )
}
