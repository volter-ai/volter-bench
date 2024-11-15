import * as React from "react"
import { cn } from "@/lib/utils"
import { Card as ShadcnCard, CardContent as ShadcnCardContent, CardHeader as ShadcnCardHeader, CardTitle as ShadcnCardTitle } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface BaseProps {
  uid: string
}

let Card = React.forwardRef<HTMLDivElement, BaseProps & React.ComponentPropsWithoutRef<typeof ShadcnCard>>(
  ({ uid, ...props }, ref) => <ShadcnCard {...props} ref={ref} />
)

let CardContent = React.forwardRef<HTMLDivElement, BaseProps & React.ComponentPropsWithoutRef<typeof ShadcnCardContent>>(
  ({ uid, ...props }, ref) => <ShadcnCardContent {...props} ref={ref} />
)

let CardHeader = React.forwardRef<HTMLDivElement, BaseProps & React.ComponentPropsWithoutRef<typeof ShadcnCardHeader>>(
  ({ uid, ...props }, ref) => <ShadcnCardHeader {...props} ref={ref} />
)

let CardTitle = React.forwardRef<HTMLParagraphElement, BaseProps & React.ComponentPropsWithoutRef<typeof ShadcnCardTitle>>(
  ({ uid, ...props }, ref) => <ShadcnCardTitle {...props} ref={ref} />
)

Card = withClickable(Card)
CardContent = withClickable(CardContent)
CardHeader = withClickable(CardHeader)
CardTitle = withClickable(CardTitle)

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  imageUrl: string
  currentHp: number
  maxHp: number
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, imageUrl, currentHp, maxHp, ...props }, ref) => {
    return (
      <Card uid={uid} ref={ref} className={cn("w-[350px]", className)} {...props}>
        <CardHeader uid={`${uid}-header`}>
          <CardTitle uid={`${uid}-title`}>{name}</CardTitle>
        </CardHeader>
        <CardContent uid={`${uid}-content`}>
          <div className="flex flex-col gap-4">
            <img 
              src={imageUrl}
              alt={name}
              className="w-full h-48 object-contain"
            />
            <div className="w-full bg-secondary h-2 rounded-full">
              <div 
                className="bg-primary h-full rounded-full transition-all"
                style={{ width: `${(currentHp / maxHp) * 100}%` }}
              />
            </div>
            <div className="text-sm text-right">
              {currentHp} / {maxHp} HP
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard, Card, CardContent, CardHeader, CardTitle }
