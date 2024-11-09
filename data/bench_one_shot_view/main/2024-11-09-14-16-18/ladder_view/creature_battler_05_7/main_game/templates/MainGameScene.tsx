import { useCurrentButtons } from "@/lib/useChoices.ts"
import { Shield, Sword, ArrowLeft } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
import { Button } from "@/components/ui/button"

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
  collections: {
    skills: Skill[]
  }
  meta: {
    prototype_id: string
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
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons()

  const playerCreature = props.data.entities?.player?.entities?.active_creature
  const opponentCreature = props.data.entities?.opponent?.entities?.active_creature
  const player = props.data.entities?.player
  const opponent = props.data.entities?.opponent

  if (!player || !opponent || !playerCreature || !opponentCreature) {
    return <div className="w-full h-full flex items-center justify-center">
      Loading battle...
    </div>
  }

  const handleSkillClick = (skillUid: string) => {
    if (availableButtonSlugs.includes(`attack:${skillUid}`)) {
      emitButtonClick(`attack:${skillUid}`)
    }
  }

  return (
    <div className="w-full h-full flex flex-col">
      {/* Battlefield (upper 2/3) */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4 bg-gradient-to-b from-blue-50 to-green-50">
        {/* Top-left: Opponent Status */}
        <div className="flex flex-col items-start justify-end">
          <PlayerCard
            uid={opponent.uid}
            name={opponent.display_name}
            imageUrl={`/players/${opponent.uid}/avatar.png`}
          />
        </div>

        {/* Top-right: Opponent Creature */}
        <div className="flex items-center justify-center">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            imageUrl={`/creatures/${opponentCreature.meta.prototype_id}/front.png`}
            currentHp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
          />
        </div>

        {/* Bottom-left: Player Creature */}
        <div className="flex items-center justify-center">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl={`/creatures/${playerCreature.meta.prototype_id}/back.png`}
            currentHp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
        </div>

        {/* Bottom-right: Player Status */}
        <div className="flex flex-col items-end justify-start">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/players/${player.uid}/avatar.png`}
          />
        </div>
      </div>

      {/* UI Area (lower 1/3) */}
      <div className="h-1/3 p-4 bg-white border-t">
        <div className="flex flex-wrap gap-2 justify-center">
          {playerCreature.collections.skills && playerCreature.collections.skills.length > 0 && 
            playerCreature.collections.skills.map((skill) => {
              const buttonSlug = `attack:${skill.uid}`
              if (!availableButtonSlugs.includes(buttonSlug)) return null

              return (
                <SkillButton
                  key={skill.uid}
                  uid={skill.uid}
                  description={skill.description}
                  stats={{
                    damage: skill.stats.base_damage,
                    type: skill.meta.skill_type
                  }}
                  onClick={() => handleSkillClick(skill.uid)}
                >
                  {skill.display_name}
                </SkillButton>
              )
            })}
          
          {availableButtonSlugs.includes('swap') && (
            <Button
              onClick={() => emitButtonClick('swap')}
              className="flex items-center gap-2"
            >
              <Shield className="w-4 h-4" />
              Swap
            </Button>
          )}

          {availableButtonSlugs.includes('back') && (
            <Button
              onClick={() => emitButtonClick('back')}
              variant="secondary"
              className="flex items-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" />
              Back
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
