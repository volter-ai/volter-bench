import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react'
import { PlayerCard } from "@/components/ui/custom/player/player_card"
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

  const playerCreature = props.data.entities?.player_creature
  const opponentCreature = props.data.entities?.opponent_creature
  const player = props.data.entities?.player
  const opponent = props.data.entities?.opponent

  if (!playerCreature || !opponentCreature || !player || !opponent) {
    return (
      <div className="w-full h-full flex items-center justify-center">
        <p>Loading battle scene...</p>
      </div>
    )
  }

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* HUD */}
      <nav className="w-full bg-slate-800 p-4 flex justify-between items-center">
        <PlayerCard
          uid={player.uid}
          name={player.display_name}
          imageUrl="/images/player-avatar.png"
        />
        <PlayerCard
          uid={opponent.uid}
          name={opponent.display_name}
          imageUrl="/images/opponent-avatar.png"
        />
      </nav>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center px-16 bg-slate-700">
        <div className="relative">
          <span className="absolute -top-8 left-0 text-sm text-white">Your Creature</span>
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            currentHp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl="/images/default-creature.png"
          />
        </div>

        <div className="relative">
          <span className="absolute -top-8 left-0 text-sm text-white">Opponent's Creature</span>
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            currentHp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
            imageUrl="/images/default-creature.png"
          />
        </div>
      </div>

      {/* UI Region */}
      <div className="bg-slate-900 p-4 min-h-[200px]">
        <div className="grid grid-cols-2 gap-4">
          {playerCreature.collections?.skills?.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              damage={skill.stats.base_damage}
            />
          )) ?? (
            <div className="col-span-2 text-center text-gray-400">
              No skills available
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
