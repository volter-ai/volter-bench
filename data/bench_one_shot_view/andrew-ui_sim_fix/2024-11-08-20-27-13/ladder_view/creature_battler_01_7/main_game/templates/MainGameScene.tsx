import { useCurrentButtons } from "@/lib/useChoices.ts"
import { Shield, Swords } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { PlayerCard } from "@/components/ui/custom/player/player_card"

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    damage: number
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
    foe: Player
    player_creature: Creature
    foe_creature: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  if (!props.data?.entities) {
    return null
  }

  const { player, foe, player_creature, foe_creature } = props.data.entities

  if (!player || !foe || !player_creature || !foe_creature) {
    return null
  }

  return (
    <div className="h-screen w-full flex flex-col bg-background" uid="main-game-container">
      {/* HUD */}
      <nav className="h-16 border-b flex items-center justify-between px-4" uid="game-hud">
        <div className="flex items-center gap-4" uid="player-hud-section">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/players/${player.display_name.toLowerCase()}.png`}
          />
          <Shield className="w-6 h-6" />
        </div>
        <div className="flex items-center gap-2" uid="battle-title">
          <Swords className="w-6 h-6" />
          <span>Battle Scene</span>
        </div>
        <div className="flex items-center gap-4" uid="foe-hud-section">
          <Swords className="w-6 h-6" />
          <PlayerCard
            uid={foe.uid}
            name={foe.display_name}
            imageUrl={`/players/${foe.display_name.toLowerCase()}.png`}
          />
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-between px-8" uid="battlefield">
        <div className="flex flex-col items-center gap-2" uid={`creature-container-${player_creature.uid}`}>
          <span className="text-sm font-bold">Your Creature</span>
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl={`/creatures/${player_creature.display_name.toLowerCase()}.png`}
          />
        </div>

        <div className="flex flex-col items-center gap-2" uid={`creature-container-${foe_creature.uid}`}>
          <span className="text-sm font-bold">Opponent's Creature</span>
          <CreatureCard
            uid={foe_creature.uid}
            name={foe_creature.display_name}
            hp={foe_creature.stats.hp}
            maxHp={foe_creature.stats.max_hp}
            imageUrl={`/creatures/${foe_creature.display_name.toLowerCase()}.png`}
          />
        </div>
      </div>

      {/* Skills/UI Region */}
      <div className="h-1/3 border-t bg-muted/50 p-4" uid="skills-container">
        <div className="grid grid-cols-4 gap-4" uid="skills-grid">
          {player_creature.collections.skills?.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
