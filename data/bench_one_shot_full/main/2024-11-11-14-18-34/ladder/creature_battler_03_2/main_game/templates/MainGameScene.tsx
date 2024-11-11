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
  meta: {
    prototype_id: string
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
  meta: {
    prototype_id: string
  }
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

  if (!player || !opponent) {
    return <div className="h-screen bg-slate-900 text-white flex items-center justify-center">
      Loading players...
    </div>
  }

  return (
    <div className="grid grid-rows-[auto_1fr_auto] h-screen bg-slate-900 text-white">
      {/* HUD */}
      <nav className="bg-slate-800 p-4 flex justify-between items-center">
        <div className="flex items-center gap-4">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/assets/players/${player.meta.prototype_id}.png`}
          />
        </div>
        <div className="flex items-center gap-4">
          <PlayerCard
            uid={opponent.uid}
            name={opponent.display_name}
            imageUrl={`/assets/players/${opponent.meta.prototype_id}.png`}
          />
        </div>
      </nav>

      {/* Battlefield */}
      <main className="flex justify-between items-center p-8 bg-slate-700">
        <div className="flex-1 flex justify-center">
          {player_creature && (
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              currentHp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              imageUrl={`/assets/creatures/${player_creature.meta.prototype_id}.png`}
            />
          )}
        </div>

        {player_creature && (
          <div className="flex gap-4">
            <div className="flex flex-col items-center gap-2">
              <Sword className="w-6 h-6" />
              <span>{player_creature.stats.attack}</span>
            </div>
            <div className="flex flex-col items-center gap-2">
              <Shield className="w-6 h-6" />
              <span>{player_creature.stats.defense}</span>
            </div>
            <div className="flex flex-col items-center gap-2">
              <Zap className="w-6 h-6" />
              <span>{player_creature.stats.speed}</span>
            </div>
          </div>
        )}

        <div className="flex-1 flex justify-center">
          {opponent_creature && (
            <CreatureCard
              uid={opponent_creature.uid}
              name={opponent_creature.display_name}
              currentHp={opponent_creature.stats.hp}
              maxHp={opponent_creature.stats.max_hp}
              imageUrl={`/assets/creatures/${opponent_creature.meta.prototype_id}.png`}
            />
          )}
        </div>
      </main>

      {/* UI Controls */}
      <div className="bg-slate-800 rounded-t-lg p-4">
        {player_creature?.collections.skills && player_creature.collections.skills.length > 0 ? (
          <div className="grid grid-cols-2 gap-4">
            {player_creature.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                damage={skill.stats.base_damage}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-4 text-slate-400">
            No skills available
          </div>
        )}
      </div>
    </div>
  )
}
