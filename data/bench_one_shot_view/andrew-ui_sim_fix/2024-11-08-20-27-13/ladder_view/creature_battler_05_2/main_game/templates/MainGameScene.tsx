import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, SwapHorizontal } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { Button } from "@/components/ui/button"

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
  entities: {
    active_creature?: Creature
  }
}

interface GameUIData {
  entities: {
    player: Player
    opponent: Player
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player?.entities.active_creature
  const opponentCreature = props.data.entities.opponent?.entities.active_creature
  const player = props.data.entities.player
  const opponent = props.data.entities.opponent

  if (!player || !opponent) {
    return <div className="w-full h-full flex items-center justify-center">
      Loading players...
    </div>
  }

  if (!playerCreature || !opponentCreature) {
    return <div className="w-full h-full flex items-center justify-center">
      Loading creatures...
    </div>
  }

  return (
    <div className="w-full h-full flex flex-col">
      {/* Battlefield Area (upper 2/3) */}
      <div className="h-2/3 grid grid-cols-2 gap-4 p-4 bg-gradient-to-b from-sky-100 to-sky-50">
        {/* Opponent Status */}
        <div className="flex items-start justify-start">
          <PlayerCard
            uid={opponent.uid}
            name={opponent.display_name}
            imageUrl={`/players/${opponent.meta?.prototype_id || 'default'}.png`}
          />
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              imageUrl={`/creatures/${opponentCreature.meta?.prototype_id || 'default'}.png`}
              currentHp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>
        
        {/* Opponent Creature */}
        <div className="flex items-start justify-end">
          <div className="relative">
            <div className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm" />
            <img 
              src={`/creatures/${opponentCreature.meta?.prototype_id || 'default'}_front.png`}
              alt={opponentCreature.display_name}
              className="w-32 h-32 object-contain"
            />
          </div>
        </div>

        {/* Player Creature */}
        <div className="flex items-end justify-start">
          <div className="relative">
            <div className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm" />
            <img 
              src={`/creatures/${playerCreature.meta?.prototype_id || 'default'}_back.png`}
              alt={playerCreature.display_name}
              className="w-32 h-32 object-contain"
            />
          </div>
        </div>

        {/* Player Status */}
        <div className="flex items-end justify-end">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/players/${player.meta?.prototype_id || 'default'}.png`}
          />
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl={`/creatures/${playerCreature.meta?.prototype_id || 'default'}.png`}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* UI Area (lower 1/3) */}
      <div className="h-1/3 p-4 bg-white/90 border-t">
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            {availableButtonSlugs.includes('attack') && playerCreature?.collections.skills && (
              <div className="grid grid-cols-2 gap-2">
                {playerCreature.collections.skills.map(skill => (
                  skill && (
                    <SkillButton
                      key={skill.uid}
                      uid={skill.uid}
                      description={skill.description}
                      stats={{
                        damage: skill.stats.base_damage
                      }}
                    >
                      {skill.display_name}
                    </SkillButton>
                  )
                ))}
              </div>
            )}
          </div>
          <div className="space-y-2">
            {/* Regular buttons for navigation - no custom UID needed */}
            {availableButtonSlugs.includes('swap') && (
              <Button onClick={() => emitButtonClick('swap')}>
                <SwapHorizontal className="mr-2 h-4 w-4" />
                Swap
              </Button>
            )}
            {availableButtonSlugs.includes('back') && (
              <Button onClick={() => emitButtonClick('back')}>
                <ArrowLeft className="mr-2 h-4 w-4" />
                Back
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
