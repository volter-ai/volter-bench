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

  const { player, opponent, player_creature, opponent_creature } = props.data.entities

  return (
    <div className="h-screen w-screen grid grid-rows-[auto_1fr_auto] bg-slate-900 text-white">
      {/* HUD */}
      <nav className="bg-slate-800 p-4 flex justify-between items-center">
        {player && player.__type === "Player" && (
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl="/placeholder-player.png"
          />
        )}
        {opponent && opponent.__type === "Player" && (
          <PlayerCard
            uid={opponent.uid}
            name={opponent.display_name}
            imageUrl="/placeholder-opponent.png"
          />
        )}
      </nav>

      {/* Battlefield */}
      <main className="relative flex justify-between items-center p-8">
        <div className="flex-1 flex justify-center">
          {player_creature && player_creature.__type === "Creature" && (
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              currentHp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              imageUrl="/placeholder-creature.png"
            />
          )}
        </div>
        
        <div className="flex-1 flex justify-center">
          {opponent_creature && opponent_creature.__type === "Creature" && (
            <CreatureCard
              uid={opponent_creature.uid}
              name={opponent_creature.display_name}
              currentHp={opponent_creature.stats.hp}
              maxHp={opponent_creature.stats.max_hp}
              imageUrl="/placeholder-creature.png"
            />
          )}
        </div>
      </main>

      {/* Action UI */}
      <div className="bg-slate-700 p-4 rounded-t-lg">
        <div className="grid grid-cols-2 gap-4">
          {player_creature?.collections?.skills?.map((skill) => (
            skill.__type === "Skill" && (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                damage={skill.stats.base_damage}
                variant="secondary"
                className="w-full"
              />
            )
          ))}
        </div>
      </div>
    </div>
  )
}
