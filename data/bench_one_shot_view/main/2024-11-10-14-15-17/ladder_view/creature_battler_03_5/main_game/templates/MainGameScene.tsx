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
        return <div className="w-full h-screen flex items-center justify-center">
            Loading battle...
        </div>;
    }

    const renderHealthBar = (current: number, max: number) => (
        <div className="w-full bg-slate-200 rounded-full h-2">
            <div
                className="bg-emerald-600 rounded-full h-2 transition-all duration-300"
                style={{ width: `${Math.max(0, Math.min(100, (current / max) * 100))}%` }}
            />
        </div>
    );

    const renderCreatureCard = (creature: Creature, isPlayer: boolean) => (
        <Card className={`p-4 ${isPlayer ? 'ml-8' : 'mr-8'}`}>
            <div className={`flex flex-col ${isPlayer ? 'items-start' : 'items-end'}`}>
                <h2 className="text-xl font-bold">{creature.display_name}</h2>
                <div className="w-48">
                    {renderHealthBar(creature.stats.hp, creature.stats.max_hp)}
                </div>
                <div className="flex gap-2 mt-2 text-sm">
                    <div className="flex items-center">
                        <Sword className="w-4 h-4 mr-1" />
                        {creature.stats.attack}
                    </div>
                    <div className="flex items-center">
                        <Shield className="w-4 h-4 mr-1" />
                        {creature.stats.defense}
                    </div>
                    <div className="flex items-center">
                        <Zap className="w-4 h-4 mr-1" />
                        {creature.stats.speed}
                    </div>
                </div>
            </div>
        </Card>
    );

    const KNOWN_SKILLS = ['tackle', 'lick'];

    return (
        <div className="w-full h-screen flex flex-col">
            {/* HUD */}
            <div className="h-[10%] bg-slate-800 p-4 flex items-center">
                <div className="flex items-center gap-2">
                    <Heart className="text-red-500" />
                    <span className="font-bold">Battle Scene</span>
                </div>
            </div>

            {/* Battlefield */}
            <div className="h-[50%] flex justify-between items-center bg-slate-100">
                <div className="relative">
                    {renderCreatureCard(playerCreature, true)}
                    <span className="absolute -top-6 left-8 text-sm font-bold">Player</span>
                </div>
                <div className="relative">
                    {renderCreatureCard(opponentCreature, false)}
                    <span className="absolute -top-6 right-8 text-sm font-bold">Opponent</span>
                </div>
            </div>

            {/* UI Region */}
            <div className="h-[40%] bg-slate-800 p-4">
                <div className="grid grid-cols-2 gap-4">
                    {playerCreature.collections.skills?.map((skill) => {
                        const skillId = skill.meta.prototype_id;
                        if (!KNOWN_SKILLS.includes(skillId)) return null;
                        
                        return availableButtonSlugs.includes(skillId) && (
                            <Button
                                key={skill.uid}
                                onClick={() => emitButtonClick(skillId)}
                                variant="secondary"
                                className="h-auto flex flex-col items-start p-4"
                            >
                                <span className="font-bold">{skill.display_name}</span>
                                <span className="text-sm opacity-80">{skill.description}</span>
                            </Button>
                        );
                    })}
                </div>
            </div>
        </div>
    );
}
