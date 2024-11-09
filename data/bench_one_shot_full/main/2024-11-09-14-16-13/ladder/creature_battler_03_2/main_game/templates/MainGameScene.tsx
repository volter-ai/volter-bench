import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Sword, Zap } from 'lucide-react'
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
    return <div className="h-screen w-full flex items-center justify-center">
      Loading game data...
    </div>
  }

  // Ensure we have both skills and available buttons before filtering
  const skills = player_creature.collections.skills || []
  const availableSkills = availableButtonSlugs 
    ? skills.filter(skill => availableButtonSlugs.includes(skill.uid))
    : []

  return (
    <div className="h-screen w-full grid grid-rows-[auto_1fr_auto] bg-background">
      {/* HUD */}
      <nav className="flex justify-between items-center p-4 border-b">
        <div className="flex items-center gap-4">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl="/placeholder/player.png"
          />
        </div>
        <div className="flex items-center gap-4">
          <PlayerCard
            uid={opponent.uid}
            name={opponent.display_name}
            imageUrl="/placeholder/opponent.png"
          />
        </div>
      </nav>

      {/* Battlefield */}
      <div className="grid grid-cols-2 gap-8 items-center justify-center p-8">
        {/* Player Creature */}
        <div className="flex flex-col items-center gap-4">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            currentHp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl={`/creatures/${player_creature.meta.prototype_id}.png`}
          />
          <div className="flex gap-2">
            <div className="flex items-center gap-1">
              <Sword className="w-4 h-4" />
              <span>{player_creature.stats.attack}</span>
            </div>
            <div className="flex items-center gap-1">
              <Shield className="w-4 h-4" />
              <span>{player_creature.stats.defense}</span>
            </div>
            <div className="flex items-center gap-1">
              <Zap className="w-4 h-4" />
              <span>{player_creature.stats.speed}</span>
            </div>
          </div>
        </div>

        {/* Opponent Creature */}
        <div className="flex flex-col items-center gap-4">
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            currentHp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
            imageUrl={`/creatures/${opponent_creature.meta.prototype_id}.png`}
          />
          <div className="flex gap-2">
            <div className="flex items-center gap-1">
              <Sword className="w-4 h-4" />
              <span>{opponent_creature.stats.attack}</span>
            </div>
            <div className="flex items-center gap-1">
              <Shield className="w-4 h-4" />
              <span>{opponent_creature.stats.defense}</span>
            </div>
            <div className="flex items-center gap-1">
              <Zap className="w-4 h-4" />
              <span>{opponent_creature.stats.speed}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Skills Area */}
      <div className="grid grid-cols-2 gap-4 p-4 bg-muted">
        {availableSkills.length > 0 ? (
          availableSkills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              damage={skill.stats.base_damage}
              onClick={() => emitButtonClick(skill.uid)}
            />
          ))
        ) : (
          <div className="col-span-2 text-center p-4">
            {availableButtonSlugs ? 'No skills available' : 'Loading skills...'}
          </div>
        )}
      </div>
    </div>
  )
}
