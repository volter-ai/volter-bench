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
    player_creature: Creature
    opponent_creature: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  // Early return if essential data is missing
  if (!props.data?.entities) {
    return <div className="h-screen w-screen bg-slate-900 flex items-center justify-center">
      <p className="text-white">Loading game data...</p>
    </div>
  }

  const { player, opponent, player_creature, opponent_creature } = props.data.entities

  return (
    <div className="h-screen w-screen flex flex-col bg-slate-900">
      {/* HUD */}
      <nav className="h-[10%] bg-slate-800 flex items-center justify-between px-4">
        {player && player.uid && (
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/api/images/players/${player.uid}`}
          />
        )}
        {opponent && opponent.uid && (
          <PlayerCard
            uid={opponent.uid}
            name={opponent.display_name}
            imageUrl={`/api/images/players/${opponent.uid}`}
          />
        )}
      </nav>

      {/* Battlefield */}
      <div className="h-[60%] flex justify-between items-center px-16 bg-slate-700">
        {player_creature && player_creature.uid && (
          <div className="transform translate-y-4">
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              currentHp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              imageUrl={`/api/images/creatures/${player_creature.uid}`}
            />
          </div>
        )}

        {opponent_creature && opponent_creature.uid && (
          <div className="transform translate-y-4">
            <CreatureCard
              uid={opponent_creature.uid}
              name={opponent_creature.display_name}
              currentHp={opponent_creature.stats.hp}
              maxHp={opponent_creature.stats.max_hp}
              imageUrl={`/api/images/creatures/${opponent_creature.uid}`}
            />
          </div>
        )}
      </div>

      {/* UI Region */}
      <div className="h-[30%] bg-slate-800 p-4">
        <div className="grid grid-cols-2 gap-4 h-full">
          {player_creature?.collections?.skills?.map((skill) => (
            skill && skill.uid && (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                damage={skill.stats.base_damage}
                variant="secondary"
                className="h-20"
                disabled={!availableButtonSlugs.includes(skill.uid)}
              />
            )
          ))}
        </div>
      </div>
    </div>
  )
}
