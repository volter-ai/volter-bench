import { useCurrentButtons } from "@/lib/useChoices.ts"
import { Sword, ArrowLeft, SwapHorizontal } from 'lucide-react'
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
  meta: {
    prototype_id: string
  }
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
  meta: {
    prototype_id: string
  }
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

  if (!playerCreature || !opponentCreature || !player || !opponent) {
    return <div className="text-center p-4">Loading battle...</div>
  }

  return (
    <div className="h-screen w-screen aspect-[16/9] flex flex-col bg-gradient-to-b from-blue-100 to-blue-200">
      {/* Battlefield Area (upper 2/3) */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 p-4 gap-4">
        {/* Top Left - Opponent Info */}
        <div className="flex items-center justify-start">
          <PlayerCard
            uid={opponent.uid}
            name={opponent.display_name}
            imageUrl={`/players/${opponent.meta.prototype_id}/avatar.png`}
          />
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            imageUrl={`/creatures/${opponentCreature.meta.prototype_id}/front.png`}
            currentHp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
          />
        </div>

        {/* Top Right - Opponent Creature */}
        <div className="flex items-center justify-center">
          <div className="relative">
            <img 
              src={`/creatures/${opponentCreature.meta.prototype_id}/front.png`}
              alt={opponentCreature.display_name}
              className="w-48 h-48 object-contain"
              onError={(e) => {
                e.currentTarget.src = '/creatures/placeholder.png'
              }}
            />
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
          </div>
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex items-center justify-center">
          <div className="relative">
            <img 
              src={`/creatures/${playerCreature.meta.prototype_id}/back.png`}
              alt={playerCreature.display_name}
              className="w-48 h-48 object-contain"
              onError={(e) => {
                e.currentTarget.src = '/creatures/placeholder.png'
              }}
            />
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
          </div>
        </div>

        {/* Bottom Right - Player Info */}
        <div className="flex items-center justify-end">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/players/${player.meta.prototype_id}/avatar.png`}
          />
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl={`/creatures/${playerCreature.meta.prototype_id}/back.png`}
            currentHp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
        </div>
      </div>

      {/* UI Area (lower 1/3) */}
      <div className="h-1/3 bg-white/90 p-4 flex flex-col gap-4">
        {availableButtonSlugs.includes('attack') && (
          <div className="grid grid-cols-2 gap-4">
            {playerCreature.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                description={skill.description}
                stats={{
                  damage: skill.stats.base_damage
                }}
              >
                <Sword className="mr-2 h-4 w-4" />
                {skill.display_name}
              </SkillButton>
            ))}
          </div>
        )}
        
        <div className="flex gap-4">
          {availableButtonSlugs.includes('swap') && (
            <SkillButton
              uid={`${player.uid}-swap`}
              description="Switch to another creature"
              stats={{}}
            >
              <SwapHorizontal className="mr-2 h-4 w-4" />
              Swap Creature
            </SkillButton>
          )}
          
          {availableButtonSlugs.includes('back') && (
            <SkillButton
              uid={`${player.uid}-back`}
              description="Return to previous screen"
              stats={{}}
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back
            </SkillButton>
          )}
        </div>
      </div>
    </div>
  )
}
