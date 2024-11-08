import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Sword } from 'lucide-react'
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
  meta: {
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
  }
  meta: {
    prototype_id: string
  }
  collections: {
    skills: Skill[]
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
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

  // Verify all required entities exist and have correct types
  if (!player_creature || player_creature.__type !== "Creature" ||
      !opponent_creature || opponent_creature.__type !== "Creature" ||
      !player || player.__type !== "Player" ||
      !opponent || opponent.__type !== "Player") {
    return <div className="w-full h-full flex items-center justify-center">
      Loading battle...
    </div>
  }

  return (
    <div className="w-full h-full aspect-w-16 aspect-h-9 bg-gradient-to-b from-blue-50 to-blue-100">
      {/* Battlefield Area */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 p-4 gap-4">
        {/* Opponent Info (Top Left) */}
        <div className="flex items-start justify-start">
          <PlayerCard
            uid={opponent.uid}
            name={opponent.display_name}
            imageUrl={`/players/${opponent.meta?.prototype_id || 'default'}.png`}
          />
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            imageUrl={`/creatures/${opponent_creature.meta?.prototype_id || 'default'}_front.png`}
            currentHp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
          />
        </div>

        {/* Opponent Creature (Top Right) */}
        <div className="flex items-center justify-center">
          <div className="relative">
            <div className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm" />
            <img
              src={`/creatures/${opponent_creature.meta?.prototype_id || 'default'}_front.png`}
              alt={opponent_creature.display_name}
              className="w-48 h-48 object-contain"
            />
          </div>
        </div>

        {/* Player Creature (Bottom Left) */}
        <div className="flex items-center justify-center">
          <div className="relative">
            <div className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm" />
            <img
              src={`/creatures/${player_creature.meta?.prototype_id || 'default'}_back.png`}
              alt={player_creature.display_name}
              className="w-48 h-48 object-contain"
            />
          </div>
        </div>

        {/* Player Info (Bottom Right) */}
        <div className="flex items-end justify-end">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/players/${player.meta?.prototype_id || 'default'}.png`}
          />
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            imageUrl={`/creatures/${player_creature.meta?.prototype_id || 'default'}_back.png`}
            currentHp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
          />
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 bg-white/90 p-4">
        <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
          {player_creature.collections.skills
            .filter(skill => skill.__type === "Skill")
            .map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                damage={skill.stats.base_damage}
                type={skill.meta.skill_type}
                variant="outline"
                className="w-full h-full"
              />
            ))}
        </div>
      </div>
    </div>
  )
}
