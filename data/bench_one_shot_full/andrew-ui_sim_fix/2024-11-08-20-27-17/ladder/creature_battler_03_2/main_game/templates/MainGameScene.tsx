import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords, Heart } from 'lucide-react'
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

  if (!player || !opponent || !player_creature || !opponent_creature) {
    return null
  }

  return (
    <div className="w-full h-full aspect-video bg-slate-900 flex flex-col">
      {/* HUD */}
      <nav className="w-full bg-slate-800 p-4 flex justify-between items-center">
        <PlayerCard
          uid={player.uid}
          name={player.display_name}
          imageUrl=""
          className="w-48 h-16"
        />
        
        <div className="flex gap-6">
          <div className="flex items-center gap-2">
            <Heart className="w-5 h-5 text-red-500" />
            <span>{player_creature.stats.hp}/{player_creature.stats.max_hp}</span>
          </div>
          <div className="flex items-center gap-2">
            <Shield className="w-5 h-5 text-blue-500" />
            <span>{player_creature.stats.defense}</span>
          </div>
          <div className="flex items-center gap-2">
            <Swords className="w-5 h-5 text-yellow-500" />
            <span>{player_creature.stats.attack}</span>
          </div>
        </div>

        <PlayerCard
          uid={opponent.uid}
          name={opponent.display_name}
          imageUrl=""
          className="w-48 h-16"
        />
      </nav>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center px-16 py-8">
        {/* Player Creature */}
        <div className="relative">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            currentHp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl=""
            className="transform scale-110"
          />
          <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 bg-blue-500 text-white px-3 py-1 rounded-full text-sm">
            Player
          </div>
        </div>

        {/* Opponent Creature */}
        <div className="relative">
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            currentHp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
            imageUrl=""
            className="transform scale-110"
          />
          <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 bg-red-500 text-white px-3 py-1 rounded-full text-sm">
            Opponent
          </div>
        </div>
      </div>

      {/* UI Region */}
      <div className="bg-slate-800 p-6 rounded-t-xl">
        <div className="grid grid-cols-2 gap-4 max-w-md mx-auto">
          {player_creature.collections.skills?.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              damage={skill.stats.base_damage}
              variant="secondary"
              className="w-full"
            />
          ))}
        </div>
      </div>
    </div>
  )
}
