import * as React from "react"
import { cn } from "@/lib/utils"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import withClickable from "@/lib/withClickable"

interface BaseCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
}

let CustomCard = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <Card ref={ref} {...props} />
)

let CustomCardHeader = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <CardHeader ref={ref} {...props} />
)

let CustomCardTitle = React.forwardRef<HTMLParagraphElement, BaseCardProps & React.HTMLAttributes<HTMLHeadingElement>>(
  ({ uid, ...props }, ref) => <CardTitle ref={ref} {...props} />
)

let CustomCardContent = React.forwardRef<HTMLDivElement, BaseCardProps>(
  ({ uid, ...props }, ref) => <CardContent ref={ref} {...props} />
)

CustomCard = withClickable(CustomCard)
CustomCardHeader = withClickable(CustomCardHeader)
CustomCardTitle = withClickable(CustomCardTitle)
CustomCardContent = withClickable(CustomCardContent)

interface CreatureCardProps extends React.HTMLAttributes<HTMLDivElement> {
  uid: string
  name: string
  hp: number
  imageUrl: string
  isPlayer?: boolean
}

let CreatureCard = React.forwardRef<HTMLDivElement, CreatureCardProps>(
  ({ className, uid, name, hp, imageUrl, isPlayer, ...props }, ref) => {
    return (
      <CustomCard
        ref={ref}
        uid={uid}
        className={cn("w-[300px]", className)}
        {...props}
      >
        <CustomCardHeader uid={`${uid}-header`}>
          <CustomCardTitle uid={`${uid}-title`}>{name}</CustomCardTitle>
        </CustomCardHeader>
        <CustomCardContent uid={`${uid}-content`}>
          <div className="flex flex-col items-center gap-4">
            <img 
              src={imageUrl}
              alt={name}
              className="w-48 h-48 object-cover rounded-lg"
            />
            <div className="text-lg font-bold">
              HP: {hp}
            </div>
            {isPlayer && (
              <div className="text-sm text-muted-foreground">
                Your Creature
              </div>
            )}
          </div>
        </CustomCardContent>
      </CustomCard>
    )
  }
)

CreatureCard.displayName = "CreatureCard"

CreatureCard = withClickable(CreatureCard)

export { CreatureCard }
