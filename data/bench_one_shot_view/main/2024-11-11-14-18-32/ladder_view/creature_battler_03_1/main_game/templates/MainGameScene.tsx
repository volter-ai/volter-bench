import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap, Heart } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

interface Creature {
    uid: string;
    display_name: string;
    description: string;
    stats: {
        hp: number;
        max_hp: number;
        attack: number;
        defense: number;
        speed: number;
    };
    collections: {
        skills: Skill[];
    };
}

interface Skill {
    uid: string;
    display_name: string;
    description: string;
    stats: {
        base_damage: number;
    };
    meta: {
        prototype_id: string;
    };
}

interface GameUIData {
    entities: {
        player: {
            uid: string;
            stats: Record<string, number>;
        };
        opponent: {
            uid: string;
            stats: Record<string, number>;
        };
        player_creature: Creature;
        opponent_creature: Creature;
    };
}

export function MainGameSceneView(props: { data: GameUIData }) {
    const {
        availableButtonSlugs,
        emitButtonClick
    } = useCurrentButtons();

    const playerCreature = props.data?.entities?.player_creature;
    const opponentCreature = props.data?.entities?.opponent_creature;

    if (!playerCreature || !opponentCreature) {
        return <div className="flex items-center justify-center w-full h-full">
            Loading battle...
        </div>;
    }

    const renderHealthBar = (current: number, max: number) => (
        <div className="w-full bg-secondary h-2 rounded">
            <div
                className="bg-primary h-2 rounded transition-all"
                style={{ width: `${Math.max(0, Math.min(100, (current / max) * 100))}%` }}
            />
        </div>
    );

    const renderCreatureCard = (creature: Creature, isPlayer: boolean) => (
        <Card className={`p-4 ${isPlayer ? 'mr-auto' : 'ml-auto'}`}>
            <div className="flex flex-col gap-2">
                <div className="flex justify-between items-center">
                    <h3 className="font-bold">{creature.display_name}</h3>
                    <span>{creature.stats.hp}/{creature.stats.max_hp}</span>
                </div>
                {renderHealthBar(creature.stats.hp, creature.stats.max_hp)}
                <div className="flex gap-4 mt-2">
                    <div className="flex items-center gap-1">
                        <Sword className="w-4 h-4" />
                        <span>{creature.stats.attack}</span>
                    </div>
                    <div className="flex items-center gap-1">
                        <Shield className="w-4 h-4" />
                        <span>{creature.stats.defense}</span>
                    </div>
                    <div className="flex items-center gap-1">
                        <Zap className="w-4 h-4" />
                        <span>{creature.stats.speed}</span>
                    </div>
                </div>
            </div>
        </Card>
    );

    const SKILL_BUTTONS = ['tackle', 'lick'];

    return (
        <div className="flex flex-col w-full h-full">
            {/* HUD */}
            <nav className="flex items-center justify-between p-4 bg-secondary/50">
                <div className="flex items-center gap-2">
                    <Heart />
                    <span>Battle Scene</span>
                </div>
            </nav>

            {/* Battlefield */}
            <div className="flex-1 flex items-center justify-between px-8 relative">
                <div className="w-1/3">
                    <div className="text-sm mb-2">Player</div>
                    {renderCreatureCard(playerCreature, true)}
                </div>
                <div className="w-1/3 text-right">
                    <div className="text-sm mb-2">Opponent</div>
                    {renderCreatureCard(opponentCreature, false)}
                </div>
            </div>

            {/* Action UI */}
            <div className="p-4 bg-secondary/20">
                <div className="grid grid-cols-2 gap-4">
                    {SKILL_BUTTONS.map(skillId => {
                        const skill = playerCreature.collections.skills.find(
                            s => s.meta.prototype_id === skillId
                        );
                        
                        if (!skill || !availableButtonSlugs.includes(skillId)) {
                            return null;
                        }

                        return (
                            <Button
                                key={skillId}
                                onClick={() => emitButtonClick(skillId)}
                                className="w-full text-left flex flex-col items-start"
                            >
                                <span className="font-bold">{skill.display_name}</span>
                                <span className="text-sm opacity-75">{skill.description}</span>
                            </Button>
                        );
                    })}
                </div>
            </div>
        </div>
    );
}
