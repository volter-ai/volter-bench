import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react'
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
    <div className="h-screen w-full flex flex-col">
      {/* Top HUD */}
      <div className="h-1/6 bg-slate-800 flex items-center justify-between px-6">
        {player && (
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl="/placeholder-player.png"
          />
        )}
        <div className="flex items-center gap-2">
          <Shield className="h-6 w-6" />
          <span>Battle Scene</span>
          <Swords className="h-6 w-6" />
        </div>
        {opponent && (
          <PlayerCard
            uid={opponent.uid}
            name={opponent.display_name}
            imageUrl="/placeholder-opponent.png"
          />
        )}
      </div>

      {/* Battlefield */}
      <div className="h-3/6 flex justify-between items-center px-12 bg-slate-700">
        {player_creature && (
          <div className="flex flex-col items-center gap-2">
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              currentHp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              imageUrl="/placeholder-creature.png"
            />
            <span className="text-sm font-bold">Your Creature</span>
          </div>
        )}

        {opponent_creature && (
          <div className="flex flex-col items-center gap-2">
            <CreatureCard
              uid={opponent_creature.uid}
              name={opponent_creature.display_name}
              currentHp={opponent_creature.stats.hp}
              maxHp={opponent_creature.stats.max_hp}
              imageUrl="/placeholder-creature.png"
            />
            <span className="text-sm font-bold">Opponent's Creature</span>
          </div>
        )}
      </div>

      {/* Bottom UI Area */}
      <div className="h-2/6 bg-slate-800 p-6">
        <div className="grid grid-cols-2 gap-4">
          {player_creature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              damage={skill.stats.base_damage}
              variant="secondary"
            />
          ))}
        </div>
      </div>
    </div>
  )
}
